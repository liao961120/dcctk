import re
import dbm
import json
from pathlib import Path
from tqdm.auto import trange
from .utils import ngrams
from .UtilsStats import MI, Xsq, Gsq, Dice, DeltaP12, DeltaP21, FisherExact, additive_smooth


class NgramCorpus:
    """Memory efficient corpus object for computing n-gram from large corpora
    """
    
    association_measures = [
        MI, Xsq, Gsq, Dice, DeltaP21, DeltaP12, FisherExact
    ]

    def __init__(self, corpus_reader):
        self.corpus_reader = corpus_reader
        self.database = {}
        self.bigram_margins = {
            'char': {'N': 0, 'R1':0 , 'C1': 0},
            'zh_only': {'N': 0, 'R1':0 , 'C1': 0}
        }
        self.pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")
        self.db_dir = Path('dcctk.db/')
        if not self.db_dir.exists(): self.db_dir.mkdir()

    @property
    def corpus(self):
        """Return a corpus as a generator
        """
        return self.corpus_reader.get_corpus_as_gen()


    def bigram_associations(self, subcorp_idx=None, chinese_only=True, 
        sort_by="Gsq", reverse=True, fq_thresh=0, return_gen=False):

        N = self.get_corpus_size(subcorp_idx, chinese_only)
        
        output = []
        for w1w2, o11 in self.freq_distr_ngrams(2, subcorp_idx, chinese_only):
            if o11 < fq_thresh: continue
            w1, w2 = w1w2[0], w1w2[1]
            r1 = self.get_marginal_fq(w1, subcorp_idx)
            r2 = N - r1
            c1 = self.get_marginal_fq(w2, subcorp_idx)
            o12 = r1 - o11
            o21 = c1 - o11
            o22 = r2 - o21
            o11_raw = o11
            o11, o12, o21, o22, e11, e12, e21, e22 = \
                additive_smooth(o11_raw, o12, o21, o22, alpha=0)
            stats = { 
                func.__name__: func(o11, o12, o21, o22, e11, e12, e21, e22)\
                    for func in self.association_measures
            }
            stats['RawCount'] = o11_raw
            if return_gen:
                yield (w1w2, stats)
            else:
                output.append((w1w2, stats))

        if not return_gen:
            return sorted(output, reverse=reverse, key=lambda x: x[1][sort_by])


    def freq_distr_ngrams(self, n, subcorp_idx=None, chinese_only=True):
        for k, v in self.get_ngrams(n, subcorp_idx).items():
            k = k.decode('utf-8')
            if chinese_only: 
                if any(not self.pat_ch_chr.search(ch) for ch in k): continue
            yield (k, int(v))

    
    def get_ngrams(self, n, subcorp_idx=None):
        if isinstance(subcorp_idx, int):
            fn = f'{n}-grams_sc{subcorp_idx}.db'
        else:
            fn = f'{n}-grams_all.db'
        if fn in self.database: 
            return self.database[fn]
        fp = self.db_dir / fn
        if not fp.exists(): self._count_ngrams(n)
        return self.database[fn]


    def get_corpus_size(self, subcorp_idx=None, chinese_only=True):
        fn = 'corpsize_all.json'
        if chinese_only: fn = 'corpsize_zh.json'
        with open(self.db_dir / fn, encoding="utf-8") as f:
            if subcorp_idx is None:
                return sum(json.load(f))
            return json.load(f)


    def get_marginal_fq(self, char, subcorp_idx=None):
        fn = f'chr_fq_all.db'
        if isinstance(subcorp_idx, int):
            fn = f'chr_fq_sc{subcorp_idx}.db'
        return int(self.database[fn].get(char, 0))


    def _count_ngrams(self, n):
        print(f'Counting {n}-grams...')
        fp_chr_fq_all = self.db_dir / f'chr_fq_all.db'
        db_chr_fq_all = dbm.open(fp_chr_fq_all, flag='n')
        fp_all = self.db_dir / f'{n}-grams_all.db'
        db_all = dbm.open(fp_all, flag='n')
        subcorp_sizes = []
        for i, sc in enumerate(self.corpus):
            subcorp_size = 0
            subcorp_size_zh = 0
            fp_chr_fq = self.db_dir / f'chr_fq_sc{i}.db'
            db_chr_fq = dbm.open(fp_chr_fq, flag='n')
            fp = self.db_dir / f'{n}-grams_sc{i}.db'
            db = dbm.open(fp, flag='n')
            for text in sc['text']:
                for sent in text['c']:
                    for ngram in ngrams(sent, n=n):
                        # Count coocurrence
                        ng = ''.join(ngram)
                        if ng not in db:
                            db[ng] = str(1)
                            db_all[ng] = str(1)
                        else:
                            db[ng] = str(int(db[ng]) + 1)
                            db_all[ng] = str(int(db_all[ng]) + 1)
                        
                        # Count marginal
                        ch = ngram[0]
                        if ch not in db_chr_fq_all:
                            db_chr_fq_all[ch] = str(1)
                        else:
                            db_chr_fq_all[ch] = str(int(db_chr_fq_all[ch]) + 1)
                        if ch not in db_chr_fq:
                            db_chr_fq[ch] = str(1)
                        else:
                            db_chr_fq[ch] = str(int(db_chr_fq[ch]) + 1)
                        subcorp_size += 1
                        if self.pat_ch_chr.search(ch):
                            subcorp_size_zh += 1
                    # Count last character in sentence
                    ch = ngram[1]
                    if ch not in db_chr_fq_all:
                        db_chr_fq_all[ch] = str(1)
                    else:
                        db_chr_fq_all[ch] = str(int(db_chr_fq_all[ch]) + 1)
                    if ch not in db_chr_fq:
                        db_chr_fq[ch] = str(1)
                    else:
                        db_chr_fq[ch] = str(int(db_chr_fq[ch]) + 1)
                    subcorp_size += 1
                    if self.pat_ch_chr.search(ch):
                        subcorp_size_zh += 1
            db.sync()
            db.close()
            db_chr_fq.sync()
            db_chr_fq.close()
            self.database[fp.name] = dbm.open(fp, flag='r')
            self.database[fp_chr_fq.name] = dbm.open(fp_chr_fq, flag='r')
            subcorp_sizes.append( (subcorp_size, subcorp_size_zh) )

        db_all.sync()
        db_all.close()
        db_chr_fq_all.sync()
        db_chr_fq_all.close()
        self.database[fp_all.name] = dbm.open(fp_all, flag='r')
        self.database[fp_chr_fq_all.name] = dbm.open(fp_chr_fq_all, flag='r')
        self._write_corp_size(subcorp_sizes)


    def _write_corp_size(self, subcorp_sizes):
        with open(self.db_dir / "corpsize_all.json", "w", encoding="utf-8") as f:
            json.dump([x[0] for x in subcorp_sizes], f, ensure_ascii=False)
        with open(self.db_dir / "corpsize_zh.json", "w", encoding="utf-8") as f:
            json.dump([x[1] for x in subcorp_sizes], f, ensure_ascii=False)



class TextBasedCorpus:
    """Corpus object for text-based (text as unit) analysis
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")
        self.path_index = {}
        self.index_path()

    def get_texts(self, pattern, texts_as_str=False, sents_as_str=True):
        texts = {}
        for id in self._list_pattern(pattern):
            text = self.get_text(id, as_str=False)
            if text is None: continue
            if sents_as_str:
                texts[id] = '\n'.join(text)
            else:
                texts[id] = text
        if texts_as_str: 
            return '\n'.join(texts.values())
        return texts
            

    def get_text(self, id, as_str=False):
        idx = self.path_index.get(id, None)
        if idx is None or isinstance(idx, int): 
            return None
        i, j = idx
        text = self.corpus[i]['text'][j].get('c', [])
        if as_str:
            text = '\n'.join(text)
        return text


    def get_meta_by_path(self, id):
        idx = self.path_index.get(id, None)
        if idx is None:
            return {}
        if isinstance(idx, int):
            return self.corpus[idx].get('m', {})
        if isinstance(idx, tuple):
            i, j = idx
            return self.corpus[i]['text'][j].get('m', {})
        return {}


    def list_files(self, pattern, generator=False):
        if generator:
            return self._list_pattern(pattern)
        return list(self._list_pattern(pattern))


    def _list_pattern(self, pattern):
        pattern = re.compile(pattern)
        for k in self.path_index.keys():
            if pattern.search(k):
                yield k


    def index_path(self):
        print("Indexing corpus for text retrival...")
        for i in trange(len(self.corpus)):
            self.path_index[self.corpus[i]['id']] = i
            for j, text in enumerate(self.corpus[i]['text']):
                self.path_index[text['id']] = (i, j)



class IndexedCorpus(TextBasedCorpus):
    """Corpus object for fast concordance search
    """

    def __init__(self, corpus) -> None:
        TextBasedCorpus.__init__(self, corpus)
        self.index = {}
        self.index_corpus()
    

    def get_meta(self, subcorp_idx, text_idx=None, keys:list=None, include_id=True):
        if text_idx is None:
            meta = self.corpus[subcorp_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['id']
        else:
            meta = self.corpus[subcorp_idx]['text'][text_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['text'][text_idx]['id']
        if keys:
            keys.append('id')
            return { k:meta[k] for k in keys if k in meta }
        return meta


    def index_corpus(self):
        print("Indexing corpus for concordance search...")
        for i in trange(len(self.corpus)):
            for j, text in enumerate(self.corpus[i]['text']):
                for k, sent in enumerate(text['c']):
                    for l, char in enumerate(sent):
                        if char not in self.index:
                            self.index[char] = []
                        self.index[char].append( (i, j, k, l) )

