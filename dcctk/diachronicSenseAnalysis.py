from .senseAnalysis import SenseAnalysis
import pandas as pd

class DiachronicSenseAnalysis:

    def __init__(self, SA:SenseAnalysis):
        """Diachronic sense analysis based on sense clustering with Bert

        Parameters
        ----------
        SA : SenseAnalysis
            An instance of :class:`senseAnalysis.SenseAnalysis` where 
            hierarchical clustering has been performed on.
        """
        self._embeddings = SA.embeddings
        self._embeddings_plotting = SA.embeddings_plotting
        self.df = SA.hover_df

        if 'cluster' not in self.df:
            raise Exception(f'Clustering not performed yet, please run `.hierarchical_clustering()` in {SA} before passing it in.')

        # Sense distribution
        self.sense_distribution = None
        self.ts_label_map = None
        self._sense_distribution_across_time()
    
    
    def plot_sense_distribution(self, xticks:str=None, **kwargs):
        ax = self.sense_distribution.plot.bar(**kwargs)
        if xticks is None:
            ax.set_xticklabels(sorted(i for i in range(len(self.ts_label_map))), rotation=0)
        else:
            ax.set_xticklabels(sorted(l[xticks] for l in self.ts_label_map), rotation=0)


    def _sense_distribution_across_time(self):
        # Get frequency distributions
        distr = {}  
        num_of_ts = len(set(self.df.timestep))
        self.ts_label_map = [0] * num_of_ts
        time_meta_labels = self.df.columns[self.df.columns.to_series().str.contains('m.time')]
        for idx, row in self.df.iterrows():
            c = row['cluster']
            ts = int(row['timestep'])
            
            # Get distribution
            if c not in distr:
                distr[c] = [0] * num_of_ts
            distr[c][ts] += 1

            # Get timestep info
            if isinstance(self.ts_label_map[ts], int):
                self.ts_label_map[ts] = dict(row[time_meta_labels])

        d = pd.DataFrame(distr)
        d = d.reindex(sorted(d.columns), axis=1)
        total_freq = d.apply(lambda x: x.sum(), axis=1)
        for index, row in d.iterrows(): 
            d.loc[index] = row / total_freq[index]
        self.sense_distribution = d
