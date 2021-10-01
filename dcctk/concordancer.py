import re
import math
import cqls
from typing import Union
from itertools import chain
from collections import Counter
from .UtilsConcord import queryMatchToken, match_mode
from .corpusIndex import IndexedCorpus


class Concordancer(IndexedCorpus):

    _cql_default_attr = "char"
    _cql_max_quantity = 6

    def cql_search(self, cql: str, left=5, right=5):
        """Search the corpus with Corpus Query Language

        Parameters
        ----------
        cql : str
            A CQL query
        left : int, optional
            Left context size, by default 5
        right : int, optional
            Right context size, by default 5

        Yields
        -------
        dict
            A dictionary with the structure:

            .. code-block:: python

                {
                    'left': [<tk>, <tk>, ...],
                    'keyword': [<tk>, <tk>, ...],
                    'right': [<tk>, <tk>, ...],
                    'position': {
                        'subcorp_idx': <int>
                        'text_idx': <int>, 
                        'sent_idx': <int>, 
                        'tk_idx': <int>
                    },
                    'captureGroups': {
                        'verb': [<tk>],
                        'noun': [<tk>]}
                }
            
            where ``<tk>`` is a token (char), represented as a string,
        """
        queries = cqls.parse(cql, default_attr=self._cql_default_attr,max_quant=self._cql_max_quantity)

        for query in queries:
            for result in self._kwic(keywords=query, left=left, right=right):
                yield result


    def _kwic(self, keywords: list, left=5, right=5):
        # Get concordance from corpus
        search_results = self._search_keywords(keywords)
        if search_results is None: 
            return []
        for subcorp_idx, text_idx, sent_idx, tk_idx in search_results:
            cc = self._kwic_single(subcorp_idx, text_idx, sent_idx, tk_idx, tk_len=len(keywords), left=left, right=right, keywords=keywords)
            yield cc
        
        
    def _kwic_single(self, subcorp_idx, text_idx, sent_idx, tk_idx, tk_len=1, left=5, right=5, keywords:list=None):
        # Flatten doc sentences to a list of tokens
        doc = self._get_corp_data(subcorp_idx, text_idx)
        text, keyword_idx = flatten_doc_to_sent(doc['c'])

        tk_start_idx = keyword_idx(sent_idx, tk_idx)
        tk_end_idx = tk_start_idx + tk_len
        start_idx = max(tk_start_idx - left, 0)
        end_idx = min(tk_end_idx + right, len(text))

        # Get CQL labeled token positions
        captureGroups = {}
        for i, keyword in enumerate(keywords):
            if '__label__' in keyword:
                for lab in keyword.get('__label__'):
                    if lab not in captureGroups:
                        captureGroups[lab] = []
                    tk = self._get_corp_data(subcorp_idx, text_idx, sent_idx, i + tk_idx)
                    captureGroups[lab].append(tk)

        return {
            "left": text[start_idx:tk_start_idx],
            "keyword": text[tk_start_idx:tk_end_idx],
            "right": text[tk_end_idx:end_idx],
            "position": {
                "subcorp_idx": subcorp_idx,
                "text_idx": text_idx,
                "sent_idx": sent_idx,
                "tk_idx": tk_idx
            },
            "meta": {
                'time': self.get_meta(subcorp_idx, include_id=False),
                'text': self.get_meta(subcorp_idx, text_idx)
            },
            "captureGroups": captureGroups
        }


    def _search_keywords(self, keywords: list):
        #########################################################
        # Find keywords with the least number of matching results 
        #########################################################
        best_search_loc = (0, None, math.inf)
        for i, keyword in enumerate(keywords):
            results = self._search_keyword(keyword)
            num_of_matched = len(results)
            if num_of_matched == 0: 
                return None
            elif num_of_matched < best_search_loc[-1]:
                best_search_loc = (i, results, num_of_matched)
        results = best_search_loc[1]

        #######################################
        # Check other tokens around search seed
        #######################################
        keyword_anchor = {
            'length': len(keywords),
            'seed_idx': best_search_loc[0]
        }
        
        # Check all possible matching keywords
        matched_results = []
        for idx in results:
            # Get all possible matching keywords from corpus
            candidates = self._get_keywords(keyword_anchor, *idx)
            if len(candidates) != len(keywords): 
                continue
            # Check every token in keywords
            matched_num = 0
            for w_k, w_c in zip(keywords, candidates):
                if queryMatchToken(queryTerm=w_k, corpToken=w_c):
                    matched_num += 1
            if matched_num == len(keywords):
                first_keyword_idx = idx[3] - keyword_anchor['seed_idx']
                matched_results.append( [idx[0], idx[1], idx[2], first_keyword_idx] )
            
        return matched_results


    def _search_keyword(self, keyword: dict):
        """Global search of a keyword to find candidates of correct kwic instances

        Parameters
        ----------
        keyword : dict
            A dictionary specifying the matching conditions of
            the keyword:

            .. code-block:: python
            
                {
                    'match': {
                        'word': ['打'],
                        'pos': ['V.*']
                    }, 
                    'not_match': {
                        'pos': ['VH.*']
                    },
                    '__label__': ['l1']  #labels to attached to search results  
                }

        Returns
        -------
        list
            A list of matching indicies
        """
        positive_match = set()
        negative_match = set()

        # Deal with empty token {}
        if ('match' not in keyword) and ('not_match' not in keyword):
            return set(chain.from_iterable(self.index.values()))

        else:
            ########################################
            ##########   POSITIVE MATCH   ##########
            ########################################
            matching_idicies = Counter()
            chars = keyword['match'].get(self._cql_default_attr, [])
            for idx in self._intersect_search(chars):
                matching_idicies.update({idx: 1})
            
            # Get indicies that matched all given tags 
            for idx, count in matching_idicies.items():
                if count == len(keyword['match']):
                    positive_match.add(idx)
            
            # Special case: match is empty
            if len(keyword['match']) == 0:
                positive_match = set(chain.from_iterable(self.index.values()))
            
            ########################################
            ##########   NEGATIVE MATCH   ##########
            ########################################
            chars = keyword['not_match'].get(self._cql_default_attr, [])
            for idx in self._union_search(chars):
                negative_match.add(idx)

            ########################################
            #####  POSITIVE - NEGATIVE MATCH  ######
            ########################################
            positive_match.difference_update(negative_match)

        if len(positive_match) == 0:
            print(f"{keyword} not found in corpus")

        return positive_match


    def _union_search(self, values:list):
        """Given candidates values, return from corpus the position 
        of tokens matching any of the values

        Parameters
        ----------
        values : list
            A list of values to compare with
        """
        matched_indicies = set()

        for value in values:
            value, mode = match_mode(value)
            if mode == "literal":
                matched_indicies.update(self.index.get(value, []))
            else:
                for char in self.index:
                    if re.search(value, char):
                        matched_indicies.update(self.index[char])
        
        return matched_indicies


    def _intersect_search(self, values:list):
        """Given candidates values, return from corpus the position 
        of tokens matching all values

        Parameters
        ----------
        values : list
            A list of values to compare with
        """
        # Get intersections of all values
        match_count = Counter()
        for value in values:
            value, mode = match_mode(value)
            indices = set()
            if mode == "literal":
                indices = self.index.get(value, set())
            else:
                for char in self.index:
                    if re.search(value, char):
                        indices.update(self.index[char])
            
            for idx in indices:
                match_count.update({idx: 1})
        
        # Filter idicies that match all values given
        intersect_match = set()
        for idx, count in match_count.items():
            if count == len(values):
                intersect_match.add(idx)
        
        return intersect_match
        

    def _get_keywords(self, search_anchor: dict, subcorp_idx, doc_idx, sent_idx, tk_idx):
        sent = self._get_corp_data(subcorp_idx, doc_idx, sent_idx)
        start_idx = max(0, tk_idx - search_anchor['seed_idx'])
        end_idx = min(start_idx + search_anchor['length'], len(sent))
        
        return sent[start_idx:end_idx]


    def _get_corp_data(self, subcorp_idx, doc_idx=None, sent_idx=None, tk_idx=None):
        """Get corpus data by position
        """
        if doc_idx is None:
            return self.corpus[subcorp_idx]
        if sent_idx is None:
            return self.corpus[subcorp_idx]['text'][doc_idx]
        if tk_idx is None:
            return self.corpus[subcorp_idx]['text'][doc_idx]['c'][sent_idx]
        return self.corpus[subcorp_idx]['text'][doc_idx]['c'][sent_idx][tk_idx]


##################
# Helper functions
##################
def flatten_doc_to_sent(doc):
    text = ''
    sent_lengths = []
    for sent in doc:
        sent_lengths.append(len(sent))
        text += sent

    def keyword_idx(sent_idx, tk_idx):
        nonlocal sent_lengths
        for i in range(sent_idx):
            tk_idx += sent_lengths[i]
        return tk_idx
    
    return text, keyword_idx
