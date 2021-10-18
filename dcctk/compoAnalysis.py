#%%
from itertools import chain
from collections import Counter
from CompoTree import ComponentTree, Radicals, CharLexicon, IDC

ctree = ComponentTree.load()
radicals = Radicals.load()


class CompoAnalysis:

    def __init__(self, IndexedCorpus):
        """[summary]

        Parameters
        ----------
        IndexedCorpus : IndexedCorpus
            A corpus with an index of character positions. Accepts 
            :class:`dcctk.corpus.IndexedCorpus` or its super classes as inputs.
        """
        self.corpus = IndexedCorpus.corpus
        self.index = IndexedCorpus.index
        self.cc_map = {}
        self.lexicon = CharLexicon(self.index.keys(), [], [])
        self._build_cc_map()
    

    def freq_distr(self, subcorp_idx=None, text_idx=None, tp="idc"):
        """Frequency distribution of character (component)

        Parameters
        ----------
        subcorp_idx : int, optional
            Index for subcorpus, by default None, which uses the whole corpus.
        text_idx : int, optional
            Index for text in a subcorpus, by default None, which uses the 
            whole subcorpus.
        tp : str, optional
            One of :code:`chr` (Character), :code:`idc` 
            (Ideographic Description Characters), and :code:`rad` (Radical), 
            by default :code:`idc`

        Returns
        -------
        Counter
            A freqeuncy distribution.
        """
        # Character frequency distribution
        if tp == 'chr' or tp == 'char':
            return self._freq_distr_chr(subcorp_idx, text_idx)
        
        # Character component frequency distribution
        fq_compo = Counter()
        fq_ch = self._freq_distr_chr(subcorp_idx, text_idx)
        for ch, fq in fq_ch.items():
            k = "noChrData"
            if ch in self.cc_map:
                k = self.cc_map[ch].get(tp, "noCompoData")
            fq_compo.update({k: fq})
        return fq_compo


    def _freq_distr_chr(self, subcorp_idx:int=None, text_idx:int=None):
        if isinstance(text_idx, int) and isinstance(subcorp_idx, int):
            corp = self.corpus[subcorp_idx]['text'][text_idx]['c']
            return Counter(chain.from_iterable(corp))
        if isinstance(subcorp_idx, int):
            corp = (c for t in self.corpus[subcorp_idx]['text'] for c in t['c'])
            return Counter(chain.from_iterable(corp))
        
        corp = (c for sc in self.corpus for t in sc['text'] for c in t['c'])
        return Counter(chain.from_iterable(corp))


    def _build_cc_map(self):
        for ch in self.index:
            idc = ctree.ids_map.get(ch, [None])[0]
            rad = radicals.query(ch)[0]
            dph = None
            if idc is not None:
                idc = idc.idc
                dph = ctree.query(ch, use_flag="shortest", max_depth=-1)[0]
                if not isinstance(dph, str):
                    dph = dph.depth()
                else:
                    dph = 0
            if idc is None and rad == '': continue
            self.cc_map[ch] = {
                'idc': idc,
                'rad': rad,
                'dph': dph
            }
        