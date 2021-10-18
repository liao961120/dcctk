#%%
import cqls
from itertools import chain
from CompoTree import IDC

from .concordancerBase import ConcordancerBase, ConcordLine
from .subCharQuery import find_compo, load_lexicon, char_match_compo, get_radicals
from .UtilsConcord import queryMatchToken
from .UtilsSubchar import all_plain_cql, has_cql_match_type, is_subchar


class Concordancer(ConcordancerBase):
    
    lexicon = None

    def cql_search(self, cql: str, left=5, right=5):
        queries = cqls.parse(cql, default_attr=self._cql_default_attr, \
            max_quant=self._cql_max_quantity)
        
        # Cond0: all plain cql search
        if sum(all_plain_cql(q) for q in queries) == len(queries):
            for res in super(Concordancer, self).cql_search(cql, left, right):
                yield res
            return
        
        if self.lexicon is None:
            self.lexicon = load_lexicon(self.index.keys())

        for query in queries:
            # Cond1: has plain char match (plain char as anchor)
            if has_cql_match_type(query, "literal"):

                subchar_idx = [i for i, tk in enumerate(query) if is_subchar(tk)]
                query_pl = [q if i not in subchar_idx else {} \
                    for i, q in enumerate(query)]
                
                for result in self._kwic(keywords=query_pl, left=left, right=right):
                    candi = result.data['keyword']
                    matched_num = sum(1 for i in subchar_idx \
                        if char_match_compo(candi[i], query[i], self.lexicon, self.__hash__()) )
                    if matched_num == len(subchar_idx):
                        yield result
            
            # Cond2: no plain char match (compo as anchor)
            else:
                subchar_idx = [i for i, tk in enumerate(query) if is_subchar(tk)]
                tk0 = query[subchar_idx[0]]

                matched_chars = find_compo(tk0, self.lexicon, self.__hash__())

                len_query = len(query)
                keyword_anchor = {
                    'length': len_query,
                    'seed_idx': subchar_idx[0]
                }

                for idx in chain.from_iterable(self.index[c] for c in matched_chars):
                    candidates = self._get_keywords(keyword_anchor, *idx)
                    if len(candidates) != len_query: continue
                    # Check every token in keywords
                    matched_num = 0
                    for w_k, w_c in zip(query, candidates):
                        if is_subchar(w_k):
                            if char_match_compo(w_c, w_k, self.lexicon, self.__hash__()):
                                matched_num += 1
                        else: 
                            if queryMatchToken(queryTerm=w_k, corpToken=w_c):
                                matched_num += 1
                    if matched_num == len_query:
                        subcorp_idx, text_idx, sent_idx, tk_idx = \
                        idx[0], idx[1], idx[2], idx[3] - keyword_anchor['seed_idx']
                        cc = self._kwic_single(subcorp_idx, text_idx, sent_idx, tk_idx, \
                            tk_len=len_query, left=left, right=right, keywords=query)
                        yield ConcordLine(cc)
    

    @property
    def chr_idcs(self):
        return { x.name: x.value for x in IDC }

    @property
    def chr_radicals(self):
        if self.lexicon is None:
            load_lexicon(self.index.keys())
        return get_radicals(self.lexicon)
        
    @property
    def chr_phonetic_systems(self):
        return {
            'moe': {
                'phonetic_repr': 'bpm pinyin ipa'.split(),
                'tone': list('12345'),
                'src': 'https://github.com/g0v/moedict-data',
            }
        }

    @property
    def cql_attrs(self):
        return {
            "Default": ['char'],
            "CharComponent": ['compo', 'max_depth', 'idc', 'pos'],
            "CharRadical": ['radical'],
            "CharPhonetic": ["phon", "tone", "sys"]
        }

# %%
