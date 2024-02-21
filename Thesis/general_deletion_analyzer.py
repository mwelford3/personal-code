# Import required libraries/packages.
import pandas as pd
#import altair as alt

def import_data():
    datasets = {}
    with open('deletion_data.in') as deletion_infile:
        number_of_datasets = int(deletion_infile.readline().split()[-1])
        for dataset_number in range(number_of_datasets):
            dataset_name = deletion_infile.readline().split()[-1]
            dataset_sequence_number = int(deletion_infile.readline().split()[-1])
            dataset_counts_freqs_filepath = deletion_infile.readline().split()[-1]
            dataset_counts_freqs = pd.read_csv(dataset_counts_freqs_filepath)
            dataset_lengths_counts_freqs_filepath = deletion_infile.readline().split()[-1]
            dataset_lengths_counts_freqs = pd.read_csv(dataset_lengths_counts_freqs_filepath)
            dataset_id = dataset_number + 1
            
            dataset_type = ''
            if dataset_counts_freqs_filepath.startswith('pairwise'):
                dataset_type = 'pairwise'
            elif dataset_counts_freqs_filepath.startswith('multi'):
                dataset_type = 'multi'
            else:
                print("{} does not use the correct naming convention.\nDataset names should start with either 'pairwise' or 'multi'".format(dataset_counts_freqs_filepath))
                exit()
            
            datasets[dataset_name] = {'id': dataset_id,
                                      'name': dataset_name,
                                      'sequence_number':dataset_sequence_number,
                                      'type': dataset_type,
                                      'counts_freqs': dataset_counts_freqs,
                                      'lengths_counts_freqs': dataset_lengths_counts_freqs}
                                      
        return datasets
                                      
def is_frameshift(length):
    """
    Determines whether a mutation is frameshift given a length.
    """
    if length%3 == 0:
        return False
    else:
        return True
        

def preview_datasets(datasets):
    for dataset in datasets.values():
        print("Dataset: {}\n".format(dataset['name']))
        print(dataset['counts_freqs'])
        print()
       
def print_top_deletion_lengths(datasets):
    for dataset in datasets.values():
        print("Dataset: {}\n".format(dataset['name']))
        print(dataset['lengths_counts_freqs'].sort_values('Frequency', ascending=False).head(20))
        print()

def print_deletion_length_summaries(datasets):
    print('Deletion Length Summaries\n')
    for dataset in datasets.values():
        print('Dataset: {}'.format(dataset['name']))
        deletion_length_values = set(dataset['counts_freqs']['Deletion_Length'])
        print("Min:", min(deletion_length_values))
        print("Max:", max(deletion_length_values))
        print("Count:", len(deletion_length_values))
        print()
        
def print_high_frequency_deletions(dataset):
    print("High Frequency Deletions\n")
    for dataset in datasets.values():
        print("Dataset: {}\n".format(dataset['name']))
        high_frequency_deletions = dataset['counts_freqs'][dataset['counts_freqs'].Deletion_Freq > 0.001].sort_values('Deletion_Freq', ascending=False)
        print(high_frequency_deletions)
        print()

def add_frameshift_category(dataset):
    for dataset in datasets.values():
        dataset['counts_freqs']['Is_Frameshift'] = dataset['counts_freqs']['Deletion_Length'].apply(is_frameshift)
        
def add_amino_acid_positions(datasets):
    for dataset in datasets.values():
        dataset['counts_freqs']['Starting_Amino_Acid_Position'] = ((dataset['counts_freqs'].Starting_Nucleotide_Position - 1) // 3 + 1)

        dataset['counts_freqs']['Ending_Amino_Acid_Position'] = ((dataset['counts_freqs'].Ending_Nucleotide_Position - 1) // 3 + 1)        
        
if __name__ == '__main__':
    datasets = import_data()
    
    add_amino_acid_positions(datasets)
    
    add_frameshift_category(datasets)
    
    preview_datasets(datasets)
    
    print_top_deletion_lengths(datasets)
    
    print_deletion_length_summaries(datasets)
    
    print_high_frequency_deletions(datasets)