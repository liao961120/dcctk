import torch
import opencc
from tqdm.auto import trange
from typing import Callable
from pathlib import Path
from transformers import BertTokenizer, BertConfig, BertModel
from .UtilsStats import cossim


class AnchiBert:

    def __init__(self, model_path=None):
        if model_path is None:
            model_path = 'AnchiBERT/'
            if not Path(model_path).is_dir():
                _download_bert_model()

        # Bert initialization
        print(f'Loading AnchiBERT model from {model_path} ...')
        config = BertConfig.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertModel.from_pretrained(model_path,config=config)

        # Traditional to simplified chinese
        self.t2s = opencc.OpenCC('t2s.json')


    def encode_sentence(self, sent:str, idx_from:int=None, idx_to:int=None, is_traditional=True):
        """Encode a raw sentence as a vector

        Parameters
        ----------
        sent : str
            The sentence to encode.
        idx_from : int, optional
            Begining index of a token in the :code:`sent`, 
            by default None.
        idx_to : int, optional
            Ending index of a token in the :code:`sent`, 
            by default None. If :code:`idx_from` or 
            :code:`idx_to` is None, the sentence would be
            encoded by summing all tokens' vectors from the
            last hidden state in the Bert model. Otherwise,
            the subset of tokens in :code:`sent` as specified 
            by :code:`(idx_from, idx_to)` are used.
        is_traditional : bool, optional
            [description], by default True

        Returns
        -------
        numpy.ndarray
            A :code:`(768,)` numpy.ndarray array.
        """
        if is_traditional: sent = self.t2s.convert(sent)
        input = self.tokenizer(sent, return_tensors="pt")
        last_hidden_state = self.model(**input)[0]

        # Sentence vector (sum all tokens together)
        if idx_from is None or idx_to is None:
            return torch.sum(last_hidden_state[0, :, :], dim=0).detach().numpy()
        # Token vector (sum subset of tokens together)
        return torch.sum(last_hidden_state[0, (idx_from+1):(idx_to+2), :], dim=0).detach().numpy()



def semantic_sort(m:AnchiBert, concord_lines:list, base_sent:str=None, base_tk:tuple=None, is_traditional=True, simil_func:Callable=cossim):
    """Sort concordance lines based on semantic similarity of
    vectors from AnchiBert model

    Parameters
    ----------
    m : AnchiBert
        Initialized AnchiBert model from 
        :class:`embeddings.AnchiBert`.
    concord_lines : list
        A list of :class:`concordancer.ConcordLine` obtained 
        from :meth:`concordancer.Concordancer.cql_search`.
    base_sent : str, optional
        The sentence used to compare with, by default None,
        which takes the first element of :code:`concord_lines`
        as the base sentence.
    base_tk : tuple, optional
        A tuple of length 2, specifying the position 
        :code:`(idx_from, idx_to)` of the keywords in
        :code:`base_sent`, by default None. If None, the
        vector is computed from summing up all token vectors in the sentence. Otherwise, only keywords' vectors are used
        to derive the vector.
    is_traditional : bool, optional
        Whether to convert traditional into simplified Chinese
        before feeding the input to AnchiBert, by default True.
        This parameter is passed to 
        :meth:`embeddings.AnchiBert.encode_sentence`.
    simil_func : Callable, optional
        Function for computing similarity between two vectors,
        by default :func:`UtilsStats.cossim`. The function 
        should take the input vectors as its two arguments and
        returns a float.

    Returns
    -------
    list
        A list of 2-tuples :code:`(<ConcordLine>, <float>)`, 
        with the second elements being the similarity scores
        to :code:`base_sent (base_tk)`.
    """
    if base_sent is None:
        base_sent, base_tk = concord_lines[0].get_kwic()
    
    if base_tk is not None:
        compare_base = m.encode_sentence(base_sent, *base_tk, is_traditional=is_traditional)
    else:
        compare_base = m.encode_sentence(base_sent, is_traditional=is_traditional)

    for i in trange(len(concord_lines)):
        result = concord_lines[i]
        sent, tk_idx = result.get_kwic()
        if base_tk is not None:
            vec = m.encode_sentence(sent, *tk_idx, is_traditional=is_traditional)
        else:
            vec = m.encode_sentence(sent, is_traditional=is_traditional)
        
        concord_lines[i] = (result, simil_func(compare_base, vec))

    return sorted(concord_lines, key=lambda x: x[1], reverse=True)



def _download_bert_model():
    print("Downloading AnchiBert model ...")
    import gdown
    gdown.download('https://drive.google.com/uc?id=1uMlNJzilEhSigIcfjTjPdYOZL9IQfHNK', output="AnchiBERT.zip")
    gdown.extractall("AnchiBERT.zip")
