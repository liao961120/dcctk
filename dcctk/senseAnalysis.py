import numpy as np
import pandas as pd
from tqdm.auto import trange
from .embeddings import AnchiBert
from .UtilsGeneral import stringify_obj, flatten


class SenseAnalysis:

    def __init__(self, concord_lines:list, bert_model:AnchiBert, is_traditional=True, token_idx:tuple=None, hover_df:pd.DataFrame=None):
        
        self.model = bert_model
        self.concords = concord_lines
        self.concords_len = len(self.concords)
        self.embeddings = np.empty((self.concords_len, 768))
        self._get_embeddings(is_traditional, token_idx)
        self.embeddings_plotting = None

        # Plotting info
        self.hover_df = hover_df
        if hover_df is None:
            hover_df = []
            for x in self.concords:
                d = {
                    'keyword': x.data['keyword'],
                    'kwic': x.data['left'] + '{' + x.data['keyword'] + '}' + x.data['right'],
                    'timestep': str(x.get_timestep()),
                }
                for k, v in flatten(x.data['meta'], parent_key='m').items():
                    d[k] = stringify_obj(v)
                hover_df.append(d)
            self.hover_df = pd.DataFrame(hover_df)
    

    def plot_embeddings(self, interactive=True, labels:str=None, **keywords):
        import umap.plot
        if self.embeddings_plotting is None:
            self.embeddings_plotting = self.embeddings_dim_reduce(dim=2, method="umap")
        labels = self.hover_df[labels] if labels is not None else None

        if interactive:
            from bokeh.plotting import show as bokeh_show
            f = umap.plot.interactive(self.embeddings_plotting, 
                            labels=labels, 
                            hover_data=self.hover_df, 
                            **keywords)
            bokeh_show(f)
        else:
            umap.plot.points(self.embeddings_plotting, labels=labels, **keywords)


    def embeddings_dim_reduce(self, dim=2, method="umap"):
        print(f"Reducing the embedding space to {dim} dimensions...")
        if method.lower() == "umap":
            import umap
            emb = umap.UMAP(n_components=dim, metric='cosine').fit(self.embeddings)
        if method.lower() == "pca":
            from sklearn.decomposition import PCA
            emb = PCA(n_components=dim).fit_transform(self.embeddings)
        return emb


    def _get_embeddings(self, is_traditional=True, token_idx:tuple=None):
        print('Computing embeddings...')
        for i in trange(self.concords_len):
            sent, tk_idx = self.concords[i].get_kwic()
            if token_idx is not None:
                tk_idx = token_idx
            self.embeddings[i] = self.model.encode_sentence(sent, *tk_idx, is_traditional=is_traditional)

