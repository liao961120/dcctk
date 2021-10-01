#%%

from dcctk.corpusReader import PlainTextReader
from dcctk.corpusIndex import InvertedIndex

corpus = PlainTextReader().corpus

# %%
ic = InvertedIndex(corpus)
# %%

# import pickle

# with open("index_nocharmap.pkl", "wb") as f:
#     pickle.dump(ic, f)
# %%
