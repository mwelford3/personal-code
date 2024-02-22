# Filename: general_deletion_analyzer.py
# Name: Michael A. Welford
# Email: thewelfmi@hotmail.com

# Import required libraries/packages.
import pandas as pd
import altair as alt
import datetime

def import_data():
    """Imports the deletion datasets into dictionaries.
       
    Returns: datasets - a dictionary containing the dataset information
    """
    
    # Initialize the datasets dictionary.
    datasets = {}
    
    # With the deletion_data.in file open:
    with open('deletion_data.in') as deletion_infile:
    
        # Read the number of datasets.
        number_of_datasets = int(deletion_infile.readline().split()[-1])
        
        # For each dataset:
        for dataset_number in range(number_of_datasets):
            # Read the dataset name.
            dataset_name = deletion_infile.readline().split()[-1]
            
            # Read the number of sequences in the dataset.
            dataset_sequence_number = int(deletion_infile.readline().split()[-1])
            
            # Read the filepath to the counts/frequencies file with unique deletions.
            dataset_counts_freqs_filepath = deletion_infile.readline().split()[-1]
            
            # Read the .csv file for counts/freqs into memory.
            dataset_counts_freqs = pd.read_csv(dataset_counts_freqs_filepath)
            
            # Read the filepath to the counts/frequencies .csv file for deletion lengths.
            dataset_lengths_counts_freqs_filepath = deletion_infile.readline().split()[-1]
            
            # Read the .csv file into memory.
            dataset_lengths_counts_freqs = pd.read_csv(dataset_lengths_counts_freqs_filepath)
            
            # Increment the dataset id number.
            dataset_id = dataset_number + 1
            
            # Get the dataset type based on the starting of the filepath.
            dataset_type = ''
            if dataset_counts_freqs_filepath.startswith('pairwise'):
                dataset_type = 'pairwise'
            elif dataset_counts_freqs_filepath.startswith('multi'):
                dataset_type = 'multi'
            else:
                print("{} does not use the correct naming convention.\nDataset names should start with either 'pairwise' or 'multi'".format(dataset_counts_freqs_filepath))
                exit()
            
            # Save the dataset information in the datasets dictionary.
            datasets[dataset_name] = {'id': dataset_id,
                                      'name': dataset_name,
                                      'sequence_number':dataset_sequence_number,
                                      'type': dataset_type,
                                      'counts_freqs': dataset_counts_freqs,
                                      'lengths_counts_freqs': dataset_lengths_counts_freqs}
                                      
        return datasets
                                      
def is_frameshift(length):
    """
    Determines whether a deletion is frameshift given a length.
    
    Parameter: length - the length of the deletion
    
    Returns: True (if the deletion is a frameshift deletion)
             False (if the deletion is not a frameshift deletion)
    """
    if length%3 == 0:
        return False
    else:
        return True
        

def preview_datasets(datasets):
    """
    Prints a preview of the count/frequencies for each dataset.
    
    Parameter: datasets - the dictionary containing the dataset information.
    """
    
    # For each dataset:
    for dataset in datasets.values():
        #Print the dataset information.
        print("Dataset: {}\n".format(dataset['name']))
        print(dataset['counts_freqs'])
        print()
       
def print_top_deletion_lengths(datasets):
    """
    Prints the top twenty deletion lengths for each dataset 
    based on the number of sequences with deletions.
    
    Parameter: datasets - the dictionary containing the dataset information.
    """
    
    # For each dataset:
    for dataset in datasets.values():
        # Print the top 20 deletion lengths.
        print("Dataset: {}\n".format(dataset['name']))
        print(dataset['lengths_counts_freqs'].sort_values('Frequency', ascending=False).head(20))
        print()

def print_top_deletion_lengths_by_occurances(datasets):
    """
    Prints the top deletion lengths by occurances.
    
    Parameter: datasets - the dictionary containing the dataset information.
    """
    # For each dataset:
    for dataset in datasets.values():
        # Print the top 20 deletion lengths by occurances.
        print("Dataset: {}\n".format(dataset['name']))
        print(dataset['counts_freqs'].groupby('Deletion_Length').sum().sort_values('Deletion_Freq', ascending=False).head(20)[['Deletion Occurances Frequency']])
        print()
        
def print_deletion_length_summaries(datasets):
    """
    Print the deletion length summaries.
    
    Parameter: datasets - the dictionary containing dataset information.
    """
    print('Deletion Length Summaries\n')
    
    # For each dataset:
    for dataset in datasets.values():
        # Print the dataset name.
        print('Dataset: {}'.format(dataset['name']))
        
        # Get the set of deletion length values.
        deletion_length_values = set(dataset['counts_freqs']['Deletion_Length'])
        
        # Print the min and max lengths and the number of different deletion lengths.
        print("Min:", min(deletion_length_values))
        print("Max:", max(deletion_length_values))
        print("Count:", len(deletion_length_values))
        print()

        
def print_high_frequency_deletions(dataset):
    """
    Print the high frequency deletions.
    
    Parameter: dataset - the dictionary containing dataset information.
    """
    
    print("High Frequency Deletions\n")
    
    # For each dataset:
    for dataset in datasets.values():
        # Print the dataset name.
        print("Dataset: {}\n".format(dataset['name']))
        
        # Get the list of high frequency deletions.
        high_frequency_deletions = dataset['counts_freqs'][dataset['counts_freqs'].Deletion_Freq > 0.001].sort_values('Deletion_Freq', ascending=False)
        
        # Print the high frequency deletions.
        print(high_frequency_deletions)
        print()

def print_top_frameshift_deletions(datasets):
    """
    Print the top 10 frameshift deletions.
    
    Parameter: datasets - the dictionary containing dataset information.
    """
    print("Top 10 Frameshift Deletions\n")
    
    # For each dataset:
    for dataset in datasets.values():
        # Print the dataset name.
        print('Dataset: {}'.format(dataset['name']))
        
        # Get the top 10 frameshift deletions.
        top_frameshift_deletions = dataset['counts_freqs'][dataset['counts_freqs'].Is_Frameshift == True].sort_values('Deletion_Freq', ascending=False).head(10)
        
        # Print the top frameshift deletions.
        print(top_frameshift_deletions)
        print()

def print_frameshift_deletion_metric_summaries(datasets):
    """
    Prints the frameshift deletion metric summaries.
    
    Parameter: datasets - the dictionary containing dataset information
    """
    print("Frameshift Summaries\n")
    
    # For each dataset:
    for dataset in datasets.values():
        print("***************************************************")
        # Print the dataset name.
        print('Dataset: {}'.format(dataset['name']))
        # Get the deletion occurances data.
        deletion_occurances_data = dataset['counts_freqs'].groupby('Is_Frameshift').sum()
        
        # Print the deletions occcurances summary.
        print("Deletion Occurances Metric:")
        print(deletion_occurances_data['Deletion Occurances Frequency'],'\n')
        
        # Print the unique deletion summaries.
        print("Unique Deletion Metric:")
        unique_deletion_frameshift_summary_data = dataset['counts_freqs'].groupby('Is_Frameshift').count()
        
        unique_deletion_frameshift_summary_data['Unique Deletion Frequency'] = unique_deletion_frameshift_summary_data.Deletion_Count / unique_deletion_frameshift_summary_data.Deletion_Count.sum()
        
        print(unique_deletion_frameshift_summary_data['Unique Deletion Frequency'])
        print()
        print("***************************************************")

def add_deletion_occurances_frequency(datasets):
    """
    Adds the deletion occurances frequency to each dataset.
    
    Parameter: datasets - the dictionary containing dataset information.
    """
    
    # For each dataset:
    for dataset in datasets.values():
        # Get the counts/frequencies data.
        data = dataset['counts_freqs']
        
        # Create the Deletion Occurances Frequencies.
        data['Deletion Occurances Frequency'] = data.Deletion_Count / data.Deletion_Count.sum()
        
        # Print a preview of the updated datasets.
        print("Printing preview of new frequency attribute for {}.".format(dataset['name']))
        print(data[['Starting_Nucleotide_Position', 'Deletion_Length', 'Deletion Occurances Frequency']])
        
def add_frameshift_category(datasets):
    """
    Add the frameshift deletion category to each dataset.
    
    Parameter: datasets - the dictionary containing dataset information
    """
    # For each dataset:
    for dataset in datasets.values():
        # Add the frameshift category as an attribute to each dataset.
        dataset['counts_freqs']['Is_Frameshift'] = dataset['counts_freqs']['Deletion_Length'].apply(is_frameshift)
        
def add_amino_acid_positions(datasets):
    """
    Adds the amino acid positions as attributes to each dataset.
    
    Parameter: datasets - the dictionary containing dataset information.
    """
    # For each dataset, add the starting amino acid position and the ending amino acid position as attributes.
    for dataset in datasets.values():
        dataset['counts_freqs']['Starting_Amino_Acid_Position'] = ((dataset['counts_freqs'].Starting_Nucleotide_Position - 1) // 3 + 1)

        dataset['counts_freqs']['Ending_Amino_Acid_Position'] = ((dataset['counts_freqs'].Ending_Nucleotide_Position - 1) // 3 + 1)        

def print_unique_deletions_summaries(datasets):
    """
    Prints the unique deletion summaries.
    
    Parameter: datasets - the dictionary containing dataset information
    """
    print("Unique Deletion Length Summaries\n")
    # For each dataset:
    for dataset in datasets.values():
        # Print the dataset name.
        print('Dataset: {}'.format(dataset['name']))
        
        # Get the unique deletion data and create the unique deletion frequency attribute.
        unique_deletion_data = dataset['counts_freqs'].groupby('Deletion_Length').count()
        unique_deletion_data['Unique Deletion Frequency'] = unique_deletion_data.Deletion_Count / unique_deletion_data.Deletion_Count.sum()
        
        # Print the summary.
        print(unique_deletion_data[['Unique Deletion Frequency']].sort_values('Unique Deletion Frequency', ascending=False).head(20))
        print()

def plot_sequences_with_deletions_histograms(datasets):
    """
    Plots the length histograms for the sequences with deletions (metric 1).
    
    Parameter: datasets - the dictionary containing dataset information
    """
    # For each pair of datasets:
    for first_dataset in datasets.values():
        for second_dataset in datasets.values():
            # If the two datasets have different names:
            if first_dataset['name'] != second_dataset['name']:
                # Get the lengths data.
                first_data_deletion_lengths = first_dataset['lengths_counts_freqs']
                second_data_deletion_lengths = second_dataset['lengths_counts_freqs']
                
                # Generate plots.
                first_hist = alt.Chart(first_data_deletion_lengths).mark_bar(color='black').encode(
                             x = alt.X('Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Frequency', title='Log(Frequency)',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(type='log'))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                        "fontSize":14})
                second_hist = alt.Chart(second_data_deletion_lengths).mark_bar(color='black').encode(
                             x = alt.X('Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Frequency', title='Log(Frequency)',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(type='log'))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                        "fontSize":14})
                # Combine the top plots.
                top_hists = first_hist | second_hist
                
                # Create subsets to just show lengths <= 10.
                first_data_deletion_lengths_subset = first_data_deletion_lengths[first_data_deletion_lengths['Deletion Length'] <= 10]
                second_data_deletion_lengths_subset = second_data_deletion_lengths[second_data_deletion_lengths['Deletion Length'] <= 10]
                
                first_hist_10 = alt.Chart(first_data_deletion_lengths_subset).mark_bar(color='black').encode(
                                         x = alt.X('Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,1]))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                         "fontSize":14, "subtitle":"Lengths: 1-10"})
                                                                         
                second_hist_10 = alt.Chart(second_data_deletion_lengths_subset).mark_bar(color='black').encode(
                                         x = alt.X('Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,1]))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                         "fontSize":14, "subtitle":"Lengths: 1-10"})
                
                # Combine the bottom plots.
                bottom_hists = first_hist_10 | second_hist_10
                
                # Create the full figure.
                combined_hists = top_hists & bottom_hists
                
                # Save the figure as a .html file.
                combined_hists.save(first_dataset['name']+'_'+second_dataset['name']+'_sequences_with_deletions_histograms.html')
                
def plot_deletion_occurances_histograms(datasets):
    """
    Plots the length histograms for the deletion occurances (metric 2).
    
    Parameter: datasets - the dictionary containing dataset information
    """
    # For each pair of datasets:
    for first_dataset in datasets.values():
        for second_dataset in datasets.values():
            # If the two datasets have different names:
            if first_dataset['name'] != second_dataset['name']:
                # Get the lengths data.
                first_data_deletion_lengths = first_dataset['counts_freqs']
                second_data_deletion_lengths = second_dataset['counts_freqs']
                
                # Generate plots.
                first_hist = alt.Chart(first_data_deletion_lengths).mark_bar(color='black').encode(
                             x = alt.X('Deletion_Length', title='Deletion Length',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Deletion Occurances Frequency', title='Log(Deletion Occurances Frequency)',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(type='log'))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                        "fontSize":14})
                second_hist = alt.Chart(second_data_deletion_lengths).mark_bar(color='black').encode(
                             x = alt.X('Deletion_Length', title='Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Deletion Occurances Frequency', title='Log(Deletion Occurances Frequency)',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(type='log'))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                        "fontSize":14})
                # Combine the top plots.
                top_hists = first_hist | second_hist
                
                # Create subsets to just show lengths <= 10.
                first_data_deletion_lengths_subset = first_data_deletion_lengths[first_data_deletion_lengths['Deletion_Length'] <= 10]
                second_data_deletion_lengths_subset = second_data_deletion_lengths[second_data_deletion_lengths['Deletion_Length'] <= 10]
                
                first_hist_10 = alt.Chart(first_data_deletion_lengths_subset).mark_bar(color='black').encode(
                                         x = alt.X('Deletion_Length', title='Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Deletion Occurances Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,1]))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                         "fontSize":14, "subtitle":"Lengths: 1-10"})
                                                                         
                second_hist_10 = alt.Chart(second_data_deletion_lengths_subset).mark_bar(color='black').encode(
                                         x = alt.X('Deletion_Length', title='Deletion Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Deletion Occurances Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,1]))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                         "fontSize":14, "subtitle":"Lengths: 1-10"})
                # Combine the bottom plots.                                                        
                bottom_hists = first_hist_10 | second_hist_10
                
                # Create the full figure.
                combined_hists = top_hists & bottom_hists
                
                # Save the figure as a .html file.
                combined_hists.save(first_dataset['name']+'_'+second_dataset['name']+'_deletion_occurances_histograms.html')

def plot_unique_deletion_histograms(datasets):
    """
    Plots the length histograms for unique deletions (metric 1).
    
    Parameter: datasets - the dictionary containing dataset information
    """
    # For each pair of datasets:
    for first_dataset in datasets.values():
        for second_dataset in datasets.values():
            # If the two datasets have different names:
            if first_dataset['name'] != second_dataset['name']:
                # Get the lengths data.
                first_unique_deletion_data = first_dataset['counts_freqs'].groupby('Deletion_Length').count()
                first_unique_deletion_data['Unique Deletion Frequency'] = first_unique_deletion_data.Deletion_Count / first_unique_deletion_data.Deletion_Count.sum()
                
                second_unique_deletion_data = second_dataset['counts_freqs'].groupby('Deletion_Length').count()
                second_unique_deletion_data['Unique Deletion Frequency'] = second_unique_deletion_data.Deletion_Count / second_unique_deletion_data.Deletion_Count.sum()

                
                # Generate plots.
                first_hist = alt.Chart(first_unique_deletion_data.reset_index()).mark_bar(color='black').encode(
                             x = alt.X('Deletion_Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Unique Deletion Frequency',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,0.35]))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                        "fontSize":14})
                second_hist = alt.Chart(second_unique_deletion_data.reset_index()).mark_bar(color='black').encode(
                             x = alt.X('Deletion_Length', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                             y = alt.Y('Unique Deletion Frequency',axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,0.35]))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                        "fontSize":14})
                # Combine the top plots.
                top_hists = first_hist | second_hist
                
                # Create subsets to just show lengths <= 10.
                first_unique_deletion_data_subset = first_unique_deletion_data.reset_index()[first_unique_deletion_data.reset_index()['Deletion_Length'] <= 20]
                second_unique_deletion_data_subset = second_unique_deletion_data.reset_index()[second_unique_deletion_data.reset_index()['Deletion_Length'] <= 20]
                
                first_hist_10 = alt.Chart(first_unique_deletion_data_subset.reset_index()).mark_bar(color='black').encode(
                                         x = alt.X('Deletion_Length', axis=alt.Axis(title='Deletion Length', titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Unique Deletion Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,0.35]))).properties(title={"text":'Histogram of Deletion Lengths: '+first_dataset['name'],
                                                                         "fontSize":14})
                                                                         
                second_hist_10 = alt.Chart(second_unique_deletion_data_subset.reset_index()).mark_bar(color='black').encode(
                                         x = alt.X('Deletion_Length', axis=alt.Axis(title='Deletion Length', titleFontSize=14, labelFontSize=12),scale=alt.Scale(nice=False)),
                                         y = alt.Y('Unique Deletion Frequency', axis=alt.Axis(titleFontSize=14, labelFontSize=12),scale=alt.Scale(domain=[0,0.35]))).properties(title={"text":'Histogram of Deletion Lengths: '+second_dataset['name'],
                                                                         "fontSize":14})
                # Combine the bottom plots.                                                         
                bottom_hists = first_hist_10 | second_hist_10
                
                # Create the full figure.
                combined_hists = top_hists & bottom_hists
                
                # Save the figure as a .html file.
                combined_hists.save(first_dataset['name']+'_'+second_dataset['name']+'_unique_deletion_histograms.html')               
if __name__ == '__main__':
    # Disable the maximum number of columns shown in the output.
    pd.set_option('display.max_columns', None)
    
    print("Output of general_deletion_analyzer.py")
    print("Generated at {}.\n".format(datetime.datetime.now()))
    print("!Importing datasets.\n")
    datasets = import_data()
    
    print("!Adding amino acid positions.\n")
    add_amino_acid_positions(datasets)
    
    print("!Adding frameshift category.\n")
    add_frameshift_category(datasets)
    
    print("!Adding deletion occurances frequency.\n")
    add_deletion_occurances_frequency(datasets)
    
    print("!Previewing datasets.\n")
    preview_datasets(datasets)
    
    # Disable the maximum number of rows shown in the output.
    pd.set_option('display.max_rows', None)
    
    
    print("!Printing the top deletion lengths.\n")
    print_top_deletion_lengths(datasets)
    
    print("!Printing deletion length summaries.\n")
    print_deletion_length_summaries(datasets)
    
    print("!Printing high frequency deletions.\n")
    print_high_frequency_deletions(datasets)
    
    print("!Plotting the histograms for the sequences with deletions metric.\n")
    plot_sequences_with_deletions_histograms(datasets)
    
    print("!Printing top deletion lengths by occurances.\n")
    print_top_deletion_lengths_by_occurances(datasets)
    
    print("!Plotting the histograms for the deletion occurances metric.\n")
    plot_deletion_occurances_histograms(datasets)
    
    print("!Printing the unique deletion sumamries.\n")
    print_unique_deletions_summaries(datasets)
    
    print("!Plotting the histograms for the unique deletion metric.\n")
    plot_unique_deletion_histograms(datasets)
    
    print("!Printing the top frameshift deletions.\n")
    print_top_frameshift_deletions(datasets)
    
    print("!Printing frameshift deletion metric summaries.\n")
    print_frameshift_deletion_metric_summaries(datasets)