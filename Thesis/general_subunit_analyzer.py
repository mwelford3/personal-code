# Filename: general_subunit_analyzer.py
# Name: Michael A. Welford
# Email: thewelfmi@hotmail.com

# Import required libraries.
import pandas as pd
import altair as alt
import datetime

# Set gene constants.
LENGTH_OF_S_GENE = 3822

def import_data():
    """Imports the mutation datasets and subunit information into dictionaries.
       
    Returns: datasets - a dictionary containing the dataset information
             subunits - a dictionary containing the subunit information
    """
    # Initialize the datasets dictionary.
    datasets = {}
    
    # With subunit_data.in open:
    with open('subunit_data.in') as subunit_infile:
        # Read the number of datasets studied.
        number_of_datasets = int(subunit_infile.readline().split()[-1])
        
        # For each dataset:
        for dataset_number in range(number_of_datasets):
            # Read the name of the dataset.
            dataset_name = subunit_infile.readline().split()[-1]
            
            # Read the number of unique sequences in the dataset.
            dataset_sequence_number = int(subunit_infile.readline().split()[-1])
            
            # Read the filepath to the counts/frequencies file.
            dataset_counts_freqs_filepath = subunit_infile.readline().split()[-1]
            
            # Increment the dataset id number.
            dataset_id = dataset_number + 1
            
            # Find the dataset type based on the filename.
            dataset_type = ''
            
            # If the filepath starts with pairwise or ends with combined_mutation_counts.csv,
            # set the type as pairwise and read the dataset into memory.
            if dataset_counts_freqs_filepath.startswith('pairwise') or dataset_counts_freqs_filepath.endswith('combined_mutation_counts.csv'):
                dataset_type = 'pairwise'
                dataset_counts_freqs = pd.read_csv(dataset_counts_freqs_filepath, index_col=0)
            # Else if the filepath starts with multi or ends with new_mutation_counts_freqs_for_S_all.csv,
            # set the type as multi and read the dataset into memory.
            elif dataset_counts_freqs_filepath.startswith('multi') or dataset_counts_freqs_filepath.endswith('new_mutation_counts_freq_for_S_all.csv'):
                dataset_type = 'multi'
                dataset_counts_freqs = pd.read_csv(dataset_counts_freqs_filepath)
            # Otherwise print an error message.
            else:
                print("{} does not use the correct naming convention.\nDataset names should start with either 'pairwise' or 'multi'".format(dataset_counts_freqs_filepath))
                exit()
            # Add the dataset information to the dictionary.
            datasets[dataset_name] = {'id': dataset_id,
                                      'name': dataset_name,
                                      'sequence_number':dataset_sequence_number,
                                      'type': dataset_type,
                                      'counts_freqs': dataset_counts_freqs}
    
    # Read the csv file containing the subunit information into the subunits dictionary.    
    subunits = pd.read_csv('subunit_info.csv').to_dict('index')
                                      
    return datasets, subunits

def add_new_attributes(datasets):
    """
    Add various mutation classification attributes to the datasets as columns.
    
    Parameters: datasets - the dictionary containing the dataset information
    """
    
    # For each dataset:
    for dataset in datasets.values():
    
        # Get the counts/frequencies data.
        data = dataset['counts_freqs']
        
        # Add the nucleotide position to the dataset.
        data['Nucleotide Position'] = data['Index'] + 1
        
        # Add the amino acid position to the dataset.
        data['Amino Acid Position'] = (data['Index'] // 3) + 1
        
        # Reset the index.
        data.set_index(['Index'], inplace=True)
        
        # If the dataset is pairwise, update the column names to match those in the multi-alignment datasets.
        if dataset['type'] == 'pairwise':
            data.rename(columns={'Count': 'Substitution_Count',' Deletion Count': 'Deletion_Count'}, inplace=True)
         
        # Create an attribute for the substitutition count + deletion count.         
        data['Overall_Count'] = data.Substitution_Count + data.Deletion_Count
        
        # Create a new attributes for the positions with at least one substitution and/or deletion.
        data['At Least One'] = pd.Series((data.Substitution_Freq> 0) | (data.Deletion_Freq > 0)).astype(int)
        data['At Least One Substitution'] = pd.Series(data.Substitution_Freq> 0).astype(int)
        data['At Least One Deletion'] = pd.Series(data.Deletion_Freq > 0).astype(int)
    
    # For each dataset, preview the dataset.    
    for dataset in datasets.values():
        print('Preview Dataset: {}'.format(dataset['name']))
        print(dataset['counts_freqs'])
        print()

def print_general_summaries(datasets):
    """
    Prints the general substitution and deletion summaries for each dataset.
    
    Parameter: datasets - the dictionary containing information for each dataset
    """
    for dataset in datasets.values():
        print('Dataset: {}'.format(dataset['name']))
        data = dataset['counts_freqs']
        
        # Get the percentage of positions with at least one substitution or deletion.
        print("Percentage of positions with at least one substitution or deletion: {}%".format(sum(data['At Least One']) * 100 /LENGTH_OF_S_GENE))
        
        # Get the percentage of positions with at least one substitution.
        print("Percentage of positions with at least one substitution: {}%".format(sum(data['At Least One Substitution']) * 100 / LENGTH_OF_S_GENE))
        
        # Get the percentage of positions with at least one deletion.
        print("Percentage of positions with at least one deletion: {}%".format(sum(data['At Least One Deletion']) * 100 / LENGTH_OF_S_GENE))
        
        # Get the average number of single nucleotide mutations.
        print("Average number of single nucleotide mutations: {}".format(sum(data.Overall_Count)/ dataset['sequence_number']))
        
        # Get the average number of substitutions.
        print("Average number of substitutions: {}".format(sum(data.Substitution_Count) / dataset['sequence_number']))
        
        # Get the average number of positions with deletions
        print("Average number of positions with deletions: {}\n".format(sum(data.Deletion_Count) / dataset['sequence_number']))
        
         
    
def plot_region_lines(dataset, 
                      min_sub_freq=0,
                      min_del_freq=0,
                      region_name = 'Full S-gene',
                      start_aa_pos= 1, 
                      end_aa_pos = 1274, 
                      dataset_name="None"):
    """
    Plots the positions with substitutions or deletions in a given dataset under the passed conditions.
    
    Parameters: dataset - the dataset to plot
                min_sub_freq - the minimum substitution freqeuncy
                min_del_freq - the minimum deletion frequency
                region_name - the name of the region to plot
                start_aa_pos - the starting amino acid position in the plotting range
                end_aa_pos - the ending amino acid position in the plotting range
                dataset_name - the name of the dataset passed
    
    Returns: mutation_plot - the Altair Chart for the subunit plot
    
    Note: The default amino acid range is the whole S-gene.
    """
    # Subset the data with the above conditions.
    d = dataset[((dataset.Substitution_Freq > min_sub_freq) | (dataset.Deletion_Freq > min_del_freq)) 
                & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    # Create the mutation position plot.
    mutation_plot = alt.Chart(d).mark_bar(color='black',width=1).encode(
    x=alt.X('Nucleotide Position',
            axis=alt.Axis(title='Nucleotide Position', tickMinStep=1, titleFontSize=14, labelFontSize=12), 
            scale=alt.Scale(
                domain=[(start_aa_pos*3)-2 ,end_aa_pos*3],
                nice=False)
          ),
    y=alt.Y('At Least One', 
            title='', 
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(labels=False)),
    tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']
    ).properties(
        width=600, 
        height=100, 
        title={'text':'Nucleotide Positions in the S-Gene with At Least One Substitution or Deletion',
               'fontSize':14})
    return mutation_plot

def plot_region_lines_substitutions(dataset, 
                                    min_sub_freq=0, 
                                    region_name = 'Full S-gene',
                                    start_aa_pos= 1, 
                                    end_aa_pos = 1274, 
                                    dataset_name="None"):
    """
    Plots the positions with substitutions in a given dataset under the passed conditions.
    
    Parameters: dataset - the dataset to plot
                min_sub_freq - the minimum substitution freqeuncy
                region_name - the name of the region to plot
                start_aa_pos - the starting amino acid position in the plotting range
                end_aa_pos - the ending amino acid position in the plotting range
                dataset_name - the name of the dataset passed
    
    Returns: substitution_plot - the Altair Chart for the subunit plot
    
    Note: The default amino acid range is the whole S-gene.
    """
    
    # Subset the data with the above conditions.
    d = dataset[(dataset.Substitution_Freq > min_sub_freq) & (dataset['Amino Acid Position'] >= start_aa_pos) 
                & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    # Create the substitution position plot.
    substitution_plot = alt.Chart(d).mark_bar(color='black',width=1).encode(
    x=alt.X('Nucleotide Position',
            title='Nucleotide Position',
            axis=alt.Axis(tickMinStep=1, titleFontSize=14, labelFontSize=12),
            scale=alt.Scale(
                domain=[(start_aa_pos*3)-2 ,end_aa_pos*3],
                nice=False)),
    y=alt.Y('At Least One Substitution', 
            #title='At Least One Substitution',
            title='',
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(labels=False)),
    tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']
    ).properties(
        width=600, 
        height=75,
        title={'text':'Nucleotide Positions in the S-Gene with At Least One Substitution',
               'fontSize':14})
    return substitution_plot

def plot_region_lines_deletions(dataset, 
                                min_del_freq=0, 
                                region_name = 'Full S-gene',
                                start_aa_pos= 1, 
                                end_aa_pos = 1274, 
                                dataset_name = "None"):
    """
    Plots the positions with deletions in a given dataset under the passed conditions.
    
    Parameters: dataset - the dataset to plot
                min_del_freq - the minimum deletion freqeuncy
                region_name - the name of the region to plot
                start_aa_pos - the starting amino acid position in the plotting range
                end_aa_pos - the ending amino acid position in the plotting range
                dataset_name - the name of the dataset passed
    
    Returns: deletion_plot - the Altair Chart for the subunit plot
    
    Note: The default amino acid range is the whole S-gene.
    """
    
    # Subset the data with the above conditions.
    d = dataset[(dataset.Deletion_Freq > min_del_freq) & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    # Create the deletion position plot.
    deletion_plot = alt.Chart(d).mark_bar(color='black',width=1).encode(
    x=alt.X('Nucleotide Position',
            title='Nucleotide Position',
            axis=alt.Axis(tickMinStep=1, titleFontSize=14, labelFontSize=12),
            scale=alt.Scale(
                domain=[(start_aa_pos*3)-2 ,end_aa_pos*3],
                nice=False)),
    y=alt.Y('At Least One Deletion', 
            #title='At Least One Deletion',
            title='',
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(labels=False)),
    tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']
    ).properties(
        width=600, 
        height=75, 
        title={'text':'Nucleotide Positions in the S-Gene with At Least One Deletion',
               'fontSize':14})
    
    return deletion_plot

def construct_subplots_all_datasets(datasets, subunits, min_sub_freq, min_del_freq):
    """
    Constructs the subunit plots for multiple datasets given minimum substitution and deletion frequencies.
    
    Parameters: datasets - the dictionary containing the dataset information
                subunits - the dictionary containing the subunit information
                min_sub_freq - the minimum substitution frequency as a decimal
                min_del_freq - the minimum deletion frequency as a decimal
    """
    
    # For each subunit:
    for subunit in subunits.values():
        # Get the region name.
        region_name = subunit['name']
        
        # Get the starting and ending amino acid positions.
        start_aa = subunit['start_aa']
        end_aa = subunit['end_aa']
        
        # For each first dataset:
        for first_dataset in datasets.values():
            # Generate the top subplot.
            first_dataset_plot = construct_subplots_single_dataset(first_dataset,
                                                                    min_sub_freq,
                                                                    min_del_freq,
                                                                    region_name,
                                                                    start_aa,
                                                                    end_aa)
            # Save the plot as an html file.
            first_dataset_plot.save(first_dataset['name']+'_'+
                                    region_name+'_'+
                                    'sub_freq='+
                                    str(float(min_sub_freq))+'_'+
                                    'del_freq='+
                                    str(float(min_del_freq))+
                                    '_subunit_plot.html')
            # For each second dataset.
            for second_dataset in datasets.values():
                # If the datasets have different names:
                if first_dataset['name'] != second_dataset['name']:
                    # Create the bottom second plot.
                    second_dataset_plot = construct_subplots_single_dataset(second_dataset,
                                                                            min_sub_freq,
                                                                            min_del_freq,
                                                                            region_name,
                                                                            start_aa,
                                                                            end_aa)
                                                                            
                    # Combine the two plots.
                    combined_plot = first_dataset_plot & second_dataset_plot
                    
                    # Save the combined plot.
                    combined_plot.save(first_dataset['name']+
                                       '_vs_'+
                                       second_dataset['name']+
                                       '_'+
                                       region_name+
                                       '_'+
                                       'sub_freq='+
                                       str(float(min_sub_freq))+
                                       '_'+
                                       'del_freq='+
                                       str(float(min_del_freq))+
                                       '_subunit_plot.html')                   
            

def construct_subplots_single_dataset(dataset, min_sub_freq,min_del_freq, region_name, start_aa, end_aa):
    """
    Constructs the subunit plots for a single dataset given minimum substitution and deletion frequencies,
    a region name, and the starting and ending amino acid positions.
    
    Parameters: dataset - the single dataset being plotted
                min_sub_freq - the minimum substitution frequency as a decimal
                min_del_freq - the minimum deletion frequency as a decimal
                region_name - a string for the region name
                start_aa - the starting amino acid position
                end_aa - the ending amino acid position
                
    Returns: the combined subunit plot
    
    Note: It uses plot_region_lines, plot_region_lines_substitution, and plot_region_lines_deletion defined above.
    """
    data = dataset['counts_freqs']
    return (plot_region_lines(data, min_sub_freq,min_del_freq,region_name, start_aa,end_aa, dataset['name']) & plot_region_lines_substitutions(data, min_sub_freq,region_name, start_aa,end_aa, dataset['name'])& plot_region_lines_deletions(data, min_del_freq,region_name, start_aa,end_aa, dataset['name']))

def get_summary(first_dataset, second_dataset, start_aa_pos=1, end_aa_pos=1274):
    """
    Gets a summary of the percentage of positions with mutations in two datasets given a specific amino acid position range.
    
    Parameters: first_dataset - the first dataset
                second_dataset - the second dataset
                start_aa_pos - the starting amino acid position
                end_aa_pos - the ending amino acid position
    """
    
    # Set the dataset to the old dataset.
    data = first_dataset['counts_freqs']
    
    # Subset the dataset for the passed amino acid position range
    d =  data[(data['Amino Acid Position'] >= start_aa_pos) & (data['Amino Acid Position'] <= end_aa_pos)]
    
    # Calculate the percentages of positions with at least one of each type of mutation.
    first_percent_any_positions = d['At Least One'].sum() / d['At Least One'].count()
    first_percent_sub_positions = d['At Least One Substitution'].sum() / d['At Least One Substitution'].count()
    first_percent_del_positions = d['At Least One Deletion'].sum() / d['At Least One Deletion'].count()
    
    # Print the percentages.
    print('First Dataset: {}'.format(first_dataset['name']))
    print('Percent Any Positions: {:.2%}\nPercent Substitution Positions: {:.2%}\nPercent Deletion Positions: {:.2%}\n'.format(first_percent_any_positions,
                                                                                                                       first_percent_sub_positions,first_percent_del_positions))
    # Set the dataset to the new dataset.           
    data = second_dataset['counts_freqs']
    
    # Subset the new dataset.                                                                                                                            
    d =  data[(data['Amino Acid Position'] >= start_aa_pos) & (data['Amino Acid Position'] <= end_aa_pos)]
                                                                                                                                
    # Calculate the percentages.                                                                                                                            
    second_percent_any_positions = d['At Least One'].sum() / d['At Least One'].count()
    second_percent_sub_positions = d['At Least One Substitution'].sum() / d['At Least One Substitution'].count()
    second_percent_del_positions = d['At Least One Deletion'].sum() / d['At Least One Deletion'].count()
                                                                                                                                
    # Show the percentages for the new dataset.                                                                                                                             
    print('Second Dataset: {}'.format(second_dataset['name']))
    print('Percent Any Positions: {:.2%}\nPercent Substitution Positions: {:.2%}\nPercent Deletion Positions: {:.2%}\n'.format(second_percent_any_positions,
                                                                                                                       second_percent_sub_positions,second_percent_del_positions))
    
    # Show the numeric differences between the two datasets.                                                                                                                            
    print('Difference:')
    print('Percent Any Positions: {:.2%}\nPercent Substitution Positions: {:.2%}\nPercent Deletion Positions: {:.2%}'.format(second_percent_any_positions - first_percent_any_positions,
                                                                                                                       second_percent_sub_positions - first_percent_sub_positions,
                                                                                                                       second_percent_del_positions - first_percent_del_positions))

def get_positions_without_mutations(input_dataset, mutation_type='all',start_aa_pos=1,end_aa_pos=1274):
    """
    Gets the list positions without mutations in a dataset given a specific amino acid position range.
    
    Parameters: input_dataset - the passed dataset (as a pandas DataFrame)
                mutation_type  - the type of mutation: all -> substitution or deletion
                                              sub -> substitution
                                              del -> deletion
                start_aa_pos - the starting amino acid position
                end_aa_pos - the ending amino acid position
    
    Returns: positions_without_mutations - a DataFrame containing the list of positions without mutations of the passed type
    """
    
    dataset = input_dataset['counts_freqs']
    # If the passed mutation type is 'all',
    # get the positions without substitutions or deletions.
    if mutation_type == 'all':
        positions_without_mutations = dataset[(dataset['At Least One'] == 0) & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    # If the passed mutation type is 'sub',
    # get the positions without substitutions.
    elif mutation_type == 'sub':
        positions_without_mutations = dataset[(dataset['At Least One Substitution'] == 0) & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    # If the passed mutation type is 'del',
    # get the positions without deletions.
    elif mutation_type == 'del':
        positions_without_mutations = dataset[(dataset['At Least One Deletion'] == 0) & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
        
    return positions_without_mutations

def get_positions_above_cutoff(input_dataset, min_sub_freq=0, min_del_freq=0,start_aa_pos= 1, end_aa_pos = 1274):
    """
    Gets the list positions with mutations in a dataset with frequencies above the passed 
    cutoffs given a specific amino acid position range.
    
    Parameters: input_dataset - the passed dataset (as a pandas DataFrame)
                min_sub_freq - the minimum substitution frequency
                min_del_freq - the minimum deletion frequency
                start_aa_pos - the starting amino acid position
                end_aa_pos - the ending amino acid position
    
    Returns: positions_dataset - the DataFrame containing the positions with mutations of frequencies above the thresholds
    """
    dataset = input_dataset['counts_freqs']
    # Create the positions subset DataFrame.
    positions_dataset = dataset[((dataset.Substitution_Freq > min_sub_freq) | (dataset.Deletion_Freq > min_del_freq)) & (dataset['Amino Acid Position'] >= start_aa_pos) & (dataset['Amino Acid Position'] <= end_aa_pos)]
    
    return positions_dataset
    
def print_subunit_summaries(datasets, subunits):
    """
    Prints the subunit summaries for each subunit and for each dataset pair.
    
    Parameters: datasets - the dictionary containing the dataset information
                subunits - the dictionary containing the subunit information
    """
    print('------------------------------------------------')
    
    # Disable the maximum number of columns and rows shown in the output.
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    # For each subunit.
    for subunit in subunits.values():
        # Print the subunit name.
        print('!Subunit: {}'.format(subunit['name']))
        
        # For each pair of datasets with different names:
        for first_dataset in datasets.values():
            for second_dataset in datasets.values():
                if first_dataset['name'] != second_dataset['name']:
                
                    # Get the summary for the comparison of the two datasets in this subunit.
                    get_summary(first_dataset, second_dataset, subunit['start_aa'], subunit['end_aa'])
                    print()
                    
                    # Print the rows for positions without mutations in this subunit in the two datasets.
                    print('Positions without mutations:\n')
                    
                    # For each mutation type. ('all' = sub or del, 'sub' = substitution, and 'del' = deletion.)
                    for mutation_type in ['all', 'sub', 'del']:
                        # Print the mutation type.
                        print('Mutation Type: {}\n'.format(mutation_type))
                        
                        # Print the rows for positions in the first dataset without mutations.
                        print('First Dataset: {}'.format(first_dataset['name']))
                        positions_without_mutations = get_positions_without_mutations(first_dataset,mutation_type, subunit['start_aa'], subunit['end_aa'])
                        if not positions_without_mutations.empty:
                            print(positions_without_mutations)
                        else:
                            print('NO POSITIONS')
                        print()
                        
                        # Print the rows for positions in the second dataset without mutations.
                        print('Second Dataset: {}'.format(second_dataset['name']))
                        positions_without_mutations = get_positions_without_mutations(second_dataset,mutation_type, subunit['start_aa'], subunit['end_aa'])
                        if not positions_without_mutations.empty:
                            print(positions_without_mutations)
                        else:
                            print('NO POSITIONS')
                        print()
                    
                    # Print the rows for positions with high frequency mutations (>= 0.01) in this subunit in the two datasets.
                    print('Positions above cutoffs:\n')
                    
                    # Print the rows for positions in the first dataset with high frequency mutations.
                    print('First Dataset: {}'.format(first_dataset['name']))
                    positions_above_cutoff = get_positions_above_cutoff(first_dataset, 0.01, 0.01, subunit['start_aa'], subunit['end_aa'])
                    if not positions_above_cutoff.empty:
                        print(positions_above_cutoff)
                    else:
                        print('NO POSITIONS')
                    print()
                    
                    # Print the rows for positions in the second dataset with high frequency mutations.
                    print('Second Dataset: {}'.format(second_dataset['name']))
                    positions_above_cutoff = get_positions_above_cutoff(second_dataset, 0.01, 0.01, subunit['start_aa'], subunit['end_aa'])
                    if not positions_above_cutoff.empty:
                        print(positions_above_cutoff)
                    else:
                        print('NO POSITIONS')
                    print()
            print('**************************************')
        print('------------------------------------------------')

# If the user runs the file:       
if __name__ == '__main__':
    print("Output of general_subunit_analyzer.py")
    print("Generated at {}.\n".format(datetime.datetime.now()))
    print("!Importing dataset and subunit information.\n")
    datasets, subunits = import_data()
    
    print("!Adding mutation classification attributes.\n")
    add_new_attributes(datasets)
    
    print("!Printing general mutation summaries.\n")
    print_general_summaries(datasets)
    
    print("!Constructing mutated position plots for all datasets and subunits.")
    print("!Generating plots of positions with at least one substitution or deletion.")
    construct_subplots_all_datasets(datasets, subunits, 0, 0)
    
    print("!Generating plots of high frequency mutation positions (>= 0.01).")
    construct_subplots_all_datasets(datasets, subunits, 0.01, 0.01)
    
    
    print("\n!Printing subunit summaries.\n")
    print_subunit_summaries(datasets, subunits)

        
        
        