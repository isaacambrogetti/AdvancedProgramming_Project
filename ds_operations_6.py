from copy import deepcopy
from file_reader import *
from abc import ABC, abstractmethod

registry = []
def is_active_decorator(function):
    def wrapper(a,b):
        print(function)
        if type(function) in registry:
            print("it works!!!")
            return function(a,b)
        else:
            raise Exception("Operation is not active")
    return wrapper


class Operation(ABC):
    @abstractmethod
    @is_active_decorator
    def execute(self, dataset):
        pass


class OperationExample(Operation):
    @is_active_decorator
    def execute(self, dataset):
        new_dataset = deepcopy(dataset)
        # do stuff
        return new_dataset

class Basic_info(Operation):
    @is_active_decorator
    def execute(self, dataset):
        new_dataset = deepcopy(dataset)
        col_types = new_dataset.dtypes.to_dict()
        # i should make changes on the dataset
        return new_dataset

# not sure yet is registry would be a file, an array, a class or what
# dummy registry



class Dataset(ABC):
    @abstractmethod
    def __init__(self, filepath, *arg, **kwargs):  # suppongo devo aggiunger operation
        pass

    @abstractmethod
    def apply(self, op):
        pass


class GFF3_dataset(Dataset):
    def __init__(self, filepath):
        self.filepath = filepath
        self.__dataset = self.create_dataframe()

    def create_dataframe(self):
        return GFF3PandasReader().read(self.filepath)

    def apply(self, op: Operation):
        return op.execute(self.__dataset)



'''class basic_info(Operation):
    def execute(self, dataset: [GFF3_dataset]):
        col_types = self.__dataset.dtypes.to_dict()
        return f'{col_types}'


class id_list(Operation):
    def execute(self):
        # Obtain the list of unique sequence IDs
        seq_ids = self.__dataset['seqid'].unique().tolist()
        return f'\nseq_ids:\n {seq_ids}'''


registry.append(OperationExample)
Filepath = 'Homo_sapiens.GRCh38.85.gff3.gz'
dataset = GFF3_dataset(Filepath)
dataset.apply(OperationExample())
#print(dataset)
#print(type(op) in registry)