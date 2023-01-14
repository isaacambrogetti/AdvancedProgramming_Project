import pandas as pd
from abc import ABC, abstractmethod

class GFF3Reader(ABC):

    @abstractmethod
    def read(self, filepath):
        pass

class GFF3PandasReader(GFF3Reader):
    def read(self, filepath):
        column_names = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
        return pd.read_csv(filepath, sep='\t', names=column_names, comment='#', low_memory=False)

# specify the dtype=['start'=int, 'stop'=int]
# it is useful to make the computer use less memory