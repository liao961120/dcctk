import re
import cqls
from tqdm.auto import tqdm


class IndexedCorpus:

    def __init__(self, corpus) -> None:
        self.index = index_corpus(corpus)
        self.corpus = corpus
        self.cql_list = [
            [{'match': {'char': ['你']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}], 
            [{'match': {'char': ['你']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}, {'match': {'char': ['我']}, 'not_match': {}}]
        ]
    
    def search(self, cql_queries):
        cql_queries = self.cql_list
        pass
    
    def search_query(self, cql_query):
        for i, tk in enumerate(cql_query):
            pass


def index_corpus(corpus):
    index = {}
    for i, subcorp in tqdm(enumerate(corpus)):
        for j, text in enumerate(subcorp['text']):
            for k, sent in enumerate(text['c']):
                for l, char in enumerate(sent):
                    if char not in self.index:
                        index[char] = []
                    index[char].append( (i, j, k, l) )
    return index

