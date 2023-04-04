from abc import ABC, abstractmethod
from reader import *

def is_active_decorator(function):
    def wrapper(self, *args, **kwargs):
        if type(self).getRegistry(self) and type(args[0]).__name__ in type(self).getRegistry(self):
            return function(self, *args, **kwargs)
        else:
            raise Exception("Operation is not active")
    return wrapper

# ABC OPERATIONS       
class Operation(ABC):
    @abstractmethod
    def execute(self, dataset):
        pass

# OPERATIONS
class BasicInfo(Operation):
    def execute(self, dataset):
        col_types = dataset.dtypes.to_dict()
        new_dataset = pd.DataFrame(col_types, ["type"]).T
        return new_dataset

class IdList(Operation):
    def execute(self, dataset):
        # Obtain the list of unique sequence IDs
        seq_ids = dataset['seqid'].unique()
        new_dataframe = pd.DataFrame(seq_ids, columns=['seq_ids'])
        return new_dataframe

class UniqueOperations(Operation):
    def execute(self, dataset):
        # Obtain the dataset of unique types of operations
        operation_types = dataset['type'].unique()
        new_dataframe = pd.DataFrame(operation_types, columns=['type'])
        return new_dataframe

class NFeatures(Operation):
    def execute(self, dataset):
        # Obtain the dataset that counts the number of features provided by the same source
        source_counts = dataset['source'].value_counts()
        new_dataset = pd.DataFrame(source_counts, columns=['source'])
        return new_dataset

class NEntries(Operation):
    def execute(self, dataset):
        # Obtain the dataset that count the number of entries for each type of operation
        operation_counts = dataset['type'].value_counts()
        new_dataset = pd.DataFrame(operation_counts, columns=['type'])
        return new_dataset

class DSChromosomes(Operation):
    def execute(self, dataset):
        # Obtain the dataset containing only the information about entire chromosomes
        new_dataset = dataset[(dataset['source'] == 'GRCh38') & (dataset['type'] == 'chromosome')]
        return new_dataset

class UnassembledSeq(Operation):
    def execute(self, dataset):
        # Calculate the fraction of unassembled sequences from source GRCh38
        unassembled = dataset[(dataset['source'] == 'GRCh38') & (dataset['type'] == 'supercontig')]
        total = dataset[dataset['source'] == 'GRCh38']
        fraction = len(unassembled) / len(total)
        new_dataset = pd.DataFrame([[fraction]], columns=['fraction'])
        return new_dataset

class Filtered(Operation):
    def execute(self, dataset):
        # Obtain a new dataset containing only entries from source ensembl, havana and ensembl_havana
        filtered = dataset[dataset['source'].isin(['ensembl', 'havana', 'ensembl_havana'])]
        return filtered

class FilteredEntries(Operation):
    def execute(self, dataset):
        # Count the number of entries for each type of operation for the filtered dataset
        filtered = dataset[dataset['source'].isin(['ensembl', 'havana', 'ensembl_havana'])] 
        filtered_operation_counts = filtered['type'].value_counts()
        return filtered_operation_counts

class FilteredGeneNames(Operation):
    def execute(self, dataset):
        filtered = dataset[dataset['source'].isin(['ensembl', 'havana', 'ensembl_havana'])]
        gene_ds = filtered[filtered['type'] == 'gene'].copy()
        new_dataset = gene_ds['attributes'].str.extract('Name=([^;]+)')
        new_dataset.columns = ['gene names']
        return new_dataset



class Dataset(ABC):
    @abstractmethod
    def __init__(self, *arg, **kwargs):
        pass

    @abstractmethod
    def readDataframe(self):
        pass

    @abstractmethod
    @is_active_decorator
    def apply(self, op: Operation):
        pass

    @abstractmethod
    def getRegistry(self):
        pass

class GFF3_dataset(Dataset):
    def __init__(self):
        self.__registry = [BasicInfo.__name__, IdList.__name__, UniqueOperations.__name__, NFeatures.__name__, NEntries.__name__, 
                            DSChromosomes.__name__, UnassembledSeq.__name__, Filtered.__name__, FilteredEntries.__name__,
                            FilteredGeneNames.__name__]
        
    def readDataframe(self, filepath: str):
        self.__dataset = GFF3PandasReader(['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']).read(filepath)
        pass

    @is_active_decorator
    def apply(self, op: Operation):
        return op.execute(self.__dataset)

    def getRegistry(self):
        return self.__registry