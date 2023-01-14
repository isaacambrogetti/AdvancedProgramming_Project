from file_reader import *

# Create an instance of the GFF3PandasReader class
reader = GFF3PandasReader()

df = reader.read('Homo_sapiens.GRCh38.85.gff3.gz')
# print(df)

def my_decorator(func):
    d = {'basic_info' : True, 'id_list' : True, 'unique_operations' : True, 'n_features' : True, 'n_entries' : True,
     'ds_chromosomes' : True, 'unassebled_seq' : True, 'ds_filtered' : True, 'n_filtered_entries' : True, 'filtered_gene_names' : True}
    def wrapper(*args, **kwargs):
        print(f'\nThe decorator has the function {func.__name__}.')
        try:
            if d[func.__name__]:
                return func(*args, **kwargs)
            else:
                return print('\nThe function cannot be executed!\n')
        except KeyError:
            print('The function is not present!')
    return wrapper


@my_decorator
def basic_info():
    col_types = df.dtypes.to_dict()
    return f'\nname and type dictionary:\n {col_types}'

@my_decorator
def id_list():
    # Obtain the list of unique sequence IDs
    seq_ids = df['seqid'].unique().tolist()
    return f'\nseq_ids:\n {seq_ids}'

@my_decorator
def unique_operations():
    # Obtain the list of unique types of operations
    # .tolist() is to put them in a list as a serie of elements of the list instead of having a whole string that is considered one element
    operation_types = df['type'].unique().tolist()
    return f'\noperation_types:\n {operation_types}'

@my_decorator
def n_features():
    # Count the number of features provided by the same source
    source_counts = df['source'].value_counts()
    return f'\nsource counts:\n {source_counts}'

@my_decorator
def n_entries():
    # Count the number of entries for each type of operation
    operation_counts = df['type'].value_counts()
    return f'\noperation counts:\n {operation_counts}'

@my_decorator
def ds_chromosomes():
    # Derive a new DataFrame containing only the information about entire chromosomes
    chromosomes = df[(df['source'] == 'GRCh38') & (df['type'] == 'chromosome')]
    return f'\nchromosomes:\n {chromosomes}'

@my_decorator
def unassebled_seq():
    # Calculate the fraction of unassembled sequences from source GRCh38
    unassembled = df[(df['source'] == 'GRCh38') & (df['type'] == 'supercontig')]
    total = df[df['source'] == 'GRCh38']
    fraction = len(unassembled) / len(total)
    return f'\nfraction: \n{fraction}'

# make it work filtering the dataframe once and use it with for all the functions after
@my_decorator
def ds_filtered():
    # Obtain a new DataFrame containing only entries from source ensembl, havana and ensembl_havana
    filtered = df[df['source'].isin(['ensembl', 'havana', 'ensembl_havana'])]
    return f'\nfiltered: \n{filtered}'

@my_decorator
def n_filtered_entries():
    # Count the number of entries for each type of operation for the filtered DataFrame
    filtered = df[df['source'].isin(['ensembl', 'havana', 'ensembl_havana'])] #### it's already present in the previous func !!
    filtered_operation_counts = filtered['type'].value_counts()
    return f"\nfiltered entries:\n{filtered_operation_counts}"

@my_decorator
def filtered_gene_names():
    filtered = df[df['source'].isin(['ensembl', 'havana', 'ensembl_havana'])] #### it's already present in the previous func !!
    gene_ds = filtered[filtered['type'] == 'gene'].copy()
    # print(gene_ds)
    gene_ds['gene_name'] = gene_ds['attributes'].str.extract('Name=([^;]+)')
    return f"\ngene names:\n{gene_ds['gene_name']}"


print(basic_info())
print(id_list())
print(unique_operations())
print(n_features())
print(n_entries())
print(ds_chromosomes())
print(unassebled_seq())
print(ds_filtered())
print(n_filtered_entries())
print(filtered_gene_names())
ciao
