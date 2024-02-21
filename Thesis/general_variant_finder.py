# Filename: general_variant_finder.py
# Name: Michael A. Welford
# Email: thewelfmi@hotmail.com

# Import required libraries.
import pandas as pd
import altair as alt
import datetime

# Set gene constants.
LENGTH_OF_S_GENE = 3822


def import_counts_freqs_data():
    """Imports the mutation datasets into a dictionary.
       
       Returns: datasets - a dictionary containing the dataset information"""
    
    #Initialize the datasets dictionary.
    datasets = {}
    
    # With the finder input file open:
    with open('finder_data.in') as subunit_infile:
        # Read the number of datasets.
        number_of_datasets = int(subunit_infile.readline().split()[-1])
        
        # For each dataset in the input file:
        for dataset_number in range(number_of_datasets):
        
            # Get the dataset name.
            dataset_name = subunit_infile.readline().split()[-1]
            
            # Get the number of unique samples in the dataset.
            dataset_sequence_number = int(subunit_infile.readline().split()[-1])
            
            # Get the filepath to the counts/frequencies file.
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
                                      
                                      
    return datasets

def print_numbers_of_variant_mutations(variants):
    """
    Prints the number of nonsynonymous mutations of each type in each variant.
    
    Parameters: variants - the dictionary containing variant information.
    """
    for variant in variants.values():
        print('Variant: {}'.format(variant['name']))
        print('{0} Nonsynonymous Mutations: {1}'.format(variant['name'], len(variant['nonsynon_mutations'])))
        print('{0} S-Gene Nonsynonymous Mutations: {1}'.format(variant['name'], len(variant['nonsynon_mutations_S'])))
        print('{0} S-Gene Nonsynonymous Substitutions: {1}'.format(variant['name'], len(variant['substitutions'])))
        print('{0} S-Gene Nonsynonymous Deletions: {1}'.format(variant['name'], len(variant['deletions'])))
        print()        
        

def add_mutation_classification_attributes(datasets, variants):
    """
    Add various mutation classification attributes to the datasets as columns
    based on the different variants studied.
    
    Parameters: datasets - the dictionary containing the dataset information
                variants - the dictionary containg the variant information
    """
    
    # For each dataset:
    for dataset in datasets.values():
    
        # Get the counts/frequencies data.
        counts_freqs_data = dataset['counts_freqs']
        
        # Add the nucleotide position to the dataset.
        counts_freqs_data['Nucleotide Position'] = counts_freqs_data['Index'] + 1
        
        # Add the amino acid position to the dataset.
        counts_freqs_data['Amino Acid Position'] = (counts_freqs_data['Index'] // 3) + 1
        
        # For each variant:
        for variant in variants.values():
        
            # Add a variant to say if a position has mutated in the variant.
            counts_freqs_data['Is_'+variant['name']] = counts_freqs_data['Amino Acid Position'].isin(variant['nonsynon_mutations_S'].position)
            
            # Add Substitution and Deletion classifications.
            counts_freqs_data[variant['name']+' Substitution'] = counts_freqs_data.apply(get_variant_plotable_data, args=(variant['substitutions'],"Substitution"),axis=1)
            counts_freqs_data[variant['name']+' Deletion'] = counts_freqs_data.apply(get_variant_plotable_data, args=(variant['deletions'],"Deletion"),axis=1)
            
            # Add attribute for either substitutions or deletions.
            counts_freqs_data[variant['name']+' All'] = counts_freqs_data.apply(get_variant_plotable_data, args=(variant['nonsynon_mutations_S'],"All"),axis=1)
            
            # Create compliment attributes.
            counts_freqs_data['Non'+variant['name']+' Substitution'] = counts_freqs_data.apply(get_nonvariant_plotable_data, args=(variant['substitutions'],"Substitution"),axis=1)
            counts_freqs_data['Non'+variant['name']+' Deletion'] = counts_freqs_data.apply(get_nonvariant_plotable_data, args=(variant['deletions'],"Deletion"),axis=1)
            counts_freqs_data['Non'+variant['name']+' All'] = counts_freqs_data.apply(get_nonvariant_plotable_data, args=(variant['nonsynon_mutations_S'],"All"),axis=1)
        
        # Add boolean attribute to show which positions have at least one mutation.
        counts_freqs_data['At Least One'] = pd.Series((counts_freqs_data.Substitution_Freq > 0) | (counts_freqs_data.Deletion_Freq > 0)).astype(int)
            
        # Reset the index.        
        counts_freqs_data.set_index(['Index'], inplace=True)
        
        # Show the updated dataset.
        print('Showing updated attributes for {}'.format(dataset['name']))
        print(counts_freqs_data)
        print()
        
def import_variant_data():
    """
    Imports the variant information into memory.
    
    Returns: variants - a dictionary containing the variant information
    """
    
    # Initalize the variants dictionary.
    variants = {}
    
    # With the variant input file open:
    with open('variant_data.in') as variant_infile:
        # Read the number of variants studied.
        number_of_variants = int(variant_infile.readline().split()[-1])
        
        # For each variants:
        for variant_number in range(number_of_variants):
            # Read the variant name.
            variant_name = variant_infile.readline().rstrip()
            
            # Read the filepath for the variant mutation list. 
            variant_filepath = variant_infile.readline().split()[-1]
            
            # Read the variant mutations list file into memory.
            variant_nonsynon_mutations = pd.read_csv(variant_filepath)
            
            # Subset for S-gene mutations.
            variant_nonsynon_mutations_S = variant_nonsynon_mutations[(variant_nonsynon_mutations.gene == 'S')]
            
            # Subset for substitutions.
            variant_substitutions = variant_nonsynon_mutations_S[variant_nonsynon_mutations_S['amino acid'] != '-']
            
            # Subset for deletions.
            variant_deletions = variant_nonsynon_mutations_S[variant_nonsynon_mutations_S['amino acid'] == '-']
            
            # Add the entry to the variant dictionary.
            variants[variant_name] = {'name': variant_name,
                                      'nonsynon_mutations': variant_nonsynon_mutations,
                                      'nonsynon_mutations_S': variant_nonsynon_mutations_S,
                                      'substitutions': variant_substitutions,
                                      'deletions': variant_deletions}
    return variants

def print_variant_counts_in_each_dataset(datasets, variants):
    """
    Prints the numbers of nonsynonymous substitutions and deletions in each variant studied.
    
    Parameters: datasets - the dictionary containing the dataset information
                variants - the dictionary containing the variant information
    """
    
    # For each dataset:
    for dataset in datasets.values():
    
        print("Printing variant counts for dataset {}.".format(dataset['name']))
        
        # For each variant:
        for variant in variants.values():
            # Print the variant name.
            print('Variant: {}'.format(variant['name']))
            
            # Print the number of substitutions.
            print("Substitutions:")
            print('Substitution Count: {}'.format(get_variant_counts(variant['name'], variant['substitutions'], dataset['counts_freqs'][dataset['counts_freqs']['Substitution_Freq'] > 0], "Substitutions")))
            
            # Print the number of deletions.
            print("Deletions:")
            print('Deletion Count: {}'.format(get_variant_counts(variant['name'], variant['deletions'], dataset['counts_freqs'][dataset['counts_freqs']['Deletion_Freq'] > 0], "Deletions")))
            print()
            
def find_variant_frequency_ranks_per_dataset(datasets, variants):
    """
    Finds the variant frequency ranks for each dataset and each variant.
    
    Parameters: datasets - the dictionary containing the dataset information
                variants - the dictionary containing the variant information
                
    Returns:    frequency_ranks_data - the dictionary containing the frequency ranks data
    """
    
    # Initialize the frequency ranks dictionary.
    frequency_ranks_data = {}
    
    # For each dataset:
    for dataset in datasets.values():
        print("Finding frequency ranks for {}.".format(dataset['name']))
        
        # Initialize the frequency ranks inner dicitionary for the dataset.
        frequency_ranks_data[dataset['name']] = {}
        
        # For each variant:
        for variant in variants.values():
            # Initialize the inner dictionaries for the variant, substitutions, and deletions:
            frequency_ranks_data[dataset['name']][variant['name']] = {}
            frequency_ranks_data[dataset['name']][variant['name']]['substitutions'] = {}
            frequency_ranks_data[dataset['name']][variant['name']]['deletions'] = {}
            
            # Initialize the lists of frequency ranks data points.
            frequency_ranks_substitutions = []
            frequency_ranks_deletions = []
            
            print("\nSubstitution Frequency Ranks for {}:".format(dataset['name']))
            # For i from 0 to the number of nucleotide positions:
            for i in range(0, len(dataset['counts_freqs']) + 1, 1):
                # Get the top  i substitution positions.
                top_mutation_subset = dataset['counts_freqs'].sort_values(by=['Substitution_Freq'], ascending=False).head(i).sort_values(by=['Nucleotide Position'])
                
                # Get the number of substitution positions of the variant in the subset.
                count = get_variant_counts(variant['name'], variant['substitutions'], top_mutation_subset, "Substitutions")
                
                # Append the rank, frequency pair to the list.
                frequency_ranks_substitutions.append({'Frequency Rank':i, 'Variant Frequency':count/(len(variant['substitutions']))})
                
                # Break the loop if all the substitution positions in the variant are found.
                if count == len(variant['substitutions']):
                    break
                    
            # Convert the list to a Pandas DataFrame and set it as a dictionary value.
            frequency_ranks_data[dataset['name']][variant['name']]['substitutions'] = pd.DataFrame(frequency_ranks_substitutions)
            
            print("\nDeletion Frequency Ranks for {}:".format(dataset['name']))
            
            # For i form 0 to the number of nucleotide positions:
            for i in range(0, len(dataset['counts_freqs']) + 1, 1):
                # Get the top i  deletion positions.
                top_mutation_subset = dataset['counts_freqs'].sort_values(by=['Deletion_Freq'], ascending=False).head(i).sort_values(by=['Nucleotide Position'])
                
                # Get the number of deletion positions of the variant in the subset.
                count = get_variant_counts(variant['name'], variant['deletions'], top_mutation_subset, "Deletions")
                
                # Append the rank, frequency pair to the list.
                frequency_ranks_deletions.append({'Frequency Rank':i, 'Variant Frequency':count/(len(variant['deletions']))})
                
                # Break the loop if all deletion positions in the variant are found.
                if count == len(variant['deletions']):
                    break
                    
            # Convert the list to a Pandas DataFrame and set it as a dictionary value.
            frequency_ranks_data[dataset['name']][variant['name']]['deletions'] = pd.DataFrame(frequency_ranks_deletions)

    return frequency_ranks_data    

        
def get_variant_counts(variant_name, variant_mutation_list, subset, mutation_type):
    """
    Gets the count of variant positions found in the subset of positions.
    
    Parameter: variant_name - the name of the variant
               variant_mutation_list - the list of substitutions/deletions in the variant
               subset - the subset of positions in the form of a DataFrame
               mutation_type - the type of mutations counted
    
    Returns: count - the count of the number of BA.1 positions.
    """
    
    # Initialize the count.
    count = 0
    
    # For each matching amino acid position, increment the count.
    for pos in variant_mutation_list.position:
        if pos in list(subset['Amino Acid Position']):
            count += 1

    
    # If the count is not equal to 0, print the number of sites and the percentage of Omicron BA.1 substitutions.
    if count != 0:
        print("Number of sites: {0}".format(len(subset)))
        print("Percent of "+variant_name+" " + mutation_type + ": {0:.2%}".format(count/(len(variant_mutation_list))))
        pass
        
    # Return the count.
    return count
    
def get_variant_plotable_data(row, mutation_list, mutation_type):
    """
    Makes a plottable column to separate out a frequencies for positions
    of a specific mutation type and setting all other frequencies to 0.
    
    Parameters: row - the row in the dataset the function will be applied to
                mutation_list - the list of mutation positions that will be compared
                mutation_type - the type of mutation for which the frequencies will be returned
    """
    # If the amino acid position is found in the mutation_list (for example, BA.1 nonsynonymous substitutions):
    if row['Amino Acid Position'] in set(mutation_list.position):
        # If "Substitution" was passed, return the substitution frequency.
        if mutation_type == "Substitution":
            return row['Substitution_Freq']
        
        # If "Deletion" was passed, return the deletion frequency.
        elif mutation_type == "Deletion":
            return row['Deletion_Freq']
        
        # If "All" was passed, return the sum of the two frequencies.
        elif mutation_type == 'All':
            return row['Substitution_Freq'] + row['Deletion_Freq']
    # Otherwise, return 0.
    else:
        return 0
        
def get_nonvariant_plotable_data(row, mutation_list, mutation_type):
    """
    Makes a plottable column to separate out a frequencies for positions
    of a specific mutation type and setting all other frequencies to 0.
    
    Parameters: row - the row in the dataset the function will be applied to
                mutation_list - the list of mutation positions that will be compared
                mutation_type - the type of mutation for which the frequencies will be returned
                
    Note: This function creates the complement of get_variant_plotable_data
    """
    
    # If the position is not in the mutation list, return the respective frequency value.
    if not (row['Amino Acid Position'] in set(mutation_list.position)):
        if mutation_type == "Substitution":
            return row['Substitution_Freq']
        elif mutation_type == "Deletion":
            return row['Deletion_Freq']
        elif mutation_type == 'All':
            return row['Substitution_Freq'] + row['Deletion_Freq']
    
    # Otherwise, return 0.
    else:
        return 0

def generate_frequency_rank_plots(datasets, variants, frequency_ranks_data):
    """
    Generates the frequency rank plots and saves them as .html files.
    
    Parameters: datasets - the dictionary containing the dataset information
                variants - the dictionary containg the variant information
                frequency_ranks_data - a dictionary containing the frequency ranks data
    """
    
    # For each dataset name:
    for dataset_name in frequency_ranks_data:
    
        # Print the dataset name.
        print(dataset_name)
        
        # For each variant name:
        for variant_name in frequency_ranks_data[dataset_name]:
        
            # Print the variant name.
            print(variant_name)
            
            # Get the substitution frequency ranks.
            substitution_frequency_ranks = frequency_ranks_data[dataset_name][variant_name]['substitutions']
            
            # Create the substitution frequency ranks plot.
            substitution_frequency_ranks_plot = alt.Chart(substitution_frequency_ranks).mark_line(color='black').encode(
                                             x = alt.X('Frequency Rank',
                                             title='Frequency Rank of All Subtitution Positions in the S-gene', 
                                             axis=alt.Axis(titleFontSize=14, 
                                             labelFontSize=12)),
                                             y = alt.Y('Variant Frequency', 
                                             axis=alt.Axis(title='Cumulative '+variant_name+' S-gene Substitution Frequency', 
                                             titleFontSize=14, 
                                             labelFontSize=12)),).properties(
                                             width=900,
                                             height=450,
                                             #title={"text":"Cumulative Omicron BA.1 S-Gene Substitution Frequency vs. Frequency Rank: UniqueSeqs-Sept", "fontSize":14}
                                            )

            # Save the plot as an .html.
            substitution_frequency_ranks_plot.save('{0}_{1}_substitution_frequency_ranks_plot.html'.format(dataset_name, variant_name))
            
            # Get the deletion frequency ranks.
            deletion_frequency_ranks = frequency_ranks_data[dataset_name][variant_name]['deletions']
            
            # Create the deletion frequency ranks plot.
            deletion_frequency_ranks_plot = alt.Chart(substitution_frequency_ranks).mark_line(color='black').encode(
                                             x = alt.X('Frequency Rank',
                                             title='Frequency Rank of All Deletion Positions in the S-gene', 
                                             axis=alt.Axis(titleFontSize=14, 
                                             labelFontSize=12)),
                                             y = alt.Y('Variant Frequency', 
                                             axis=alt.Axis(title='Cumulative '+variant_name+' S-gene Deletion Frequency', 
                                             titleFontSize=14, 
                                             labelFontSize=12)),).properties(
                                             width=900,
                                             height=450,
                                             #title={"text":"Cumulative Omicron BA.1 S-Gene Substitution Frequency vs. Frequency Rank: UniqueSeqs-Sept", "fontSize":14}
                                            )

            # Save the plot as an .html.
            deletion_frequency_ranks_plot.save('{0}_{1}_deletion_frequency_ranks_plot.html'.format(dataset_name, variant_name))

def get_plotted_attributes(variant_name):
    """
    Generates a list of attributes to be plotted in the mutation frequency plots.
    
    Parameter: variant_name - the name of the variant to be plotted
    
    Returns:   plotted_attributes - the list of plotted attributes
    """
    # Initialize the list.
    plotted_attributes = []
    
    # For both the list of positions in the variant and not in the variant, for substitutions or deletions,
    # add the attribute to the list.    
    for prefix in ['Non','']:
        for mutation_type in [' Substitution', ' Deletion']:
            plotted_attributes.append(prefix + variant_name.replace('.','\.') + mutation_type)
    return plotted_attributes
    

def generate_black_and_white_mutation_frequency_plots(datasets, variants, frequency_ranks_data):
    """
    Generates the black and white mutation frequency plots.
    
    Parameters: datasets - the dictionary of dataset information
                variants - the dictionary of variant information
                frequency_ranks_data - the dictionary of frequency ranks information
    """
    
    # For each dataset:
    for dataset in datasets.values():
        # For each variant:
        for variant in variants.values():
            # Get the plotted variants:
            plotted_attributes = get_plotted_attributes(variant['name'])
            
            # Find the number of positions containing 100% of nonsynonymous substitutions for that variant.
            position_number = int(frequency_ranks_data[dataset['name']][variant['name']]['substitutions'].iloc[-1]['Frequency Rank'])
            print("\nPlotting top {} positions in {}.".format(position_number, dataset['name']))
            
            # Subset the dataset for the top 'position_number' positions.
            data_subset = dataset['counts_freqs'].sort_values(by=['Substitution_Freq'], ascending=False).head(position_number).sort_values(by=['Nucleotide Position'])
            
            # Remove attributes without peaks.
            # For each plotted attribute:
            print("Checking for empty columns.")
            for plotted_attribute in plotted_attributes:
                # Create the original format of the attribute.
                attribute = plotted_attribute.replace('\\.','.')
                # If the attribute has no peaks, remove it from the list.
                print("Checking if column {} is empty.".format(attribute))
                if sum(data_subset[attribute]) == 0:
                    print("{} is empty.".format(attribute))
                    plotted_attributes.remove(attribute)
                else:
                    print("{} is not empty.".format(attribute))
            
            # For each plotting range:
            for plotting_range in [{'name':'Whole Gene','start':1, 'end':3822},
                                            {'name': 'First Subunit', 'start':1, 'end':1000},
                                            {'name':'Second Subunit', 'start':1000, 'end':2500},
                                            {'name':'Third Subunit', 'start':2500, 'end':3822}]:
                
                # Subset for the plotting range.
                plotted_subset = data_subset[(data_subset['Nucleotide Position'] >= plotting_range['start']) & (data_subset['Nucleotide Position'] <= plotting_range['end'])]
                
                # Generate the top plot.
                plot_top = alt.Chart(plotted_subset).transform_fold(plotted_attributes).mark_bar(width=1, color='black').encode(
                           x =alt.X('Nucleotide Position', axis=alt.Axis(title='Nucleotide Positions of the S-gene', titleFontSize=14, labelFontSize=12), scale=alt.Scale(nice=False)),
                           y= alt.Y('value:Q', scale=alt.Scale(domain=[0,1]),axis=alt.Axis(title='Mutation Frequency', titleFontSize=14, labelFontSize=12)),
                           #color=alt.Color('key:N', scale=alt.Scale(range=category_colors), title='Mutation Category'),
                           tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']).properties(
                           width=800,
                           height=150,
                           #title={"text":'Mutation Frequency vs. S-Gene Nucleic Acid Index: Subset of UniqueSeqs-Sept Containing All Omicron S-Gene BA.1 Substitutions', "fontSize":14}
                        )
                
                # Add the subplots dividing the mutation category as rows.
                subplots_bottom = alt.Chart(plotted_subset).transform_fold(plotted_attributes).mark_bar(width=1, color='black').encode(
                x =alt.X('Nucleotide Position', axis=alt.Axis(title='Nucleotide Positions of the S-gene', titleFontSize=14, labelFontSize=12), scale=alt.Scale(nice=False)),
                y= alt.Y('value:Q', scale=alt.Scale(domain=[0,1]), axis=alt.Axis(title='Mutation Frequency', titleFontSize=12, labelFontSize=12)),
                #color=alt.Color('key:N', scale=alt.Scale(range=category_colors), title='Mutation Category'),
                tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq'],
                row=alt.Row('key:N', title='Mutation Category', header=alt.Header(titleFontSize=14,labelFontSize=12))).properties(
                width=800,
                height=150,
                #title='Mutation Frequency vs. S-Gene Nucleic Acid Index: Pre-Omicron Mutation Subset Containing All Omicron S-Gene BA.1 Substitutions'
                ).resolve_scale(x='independent')
                
                # Save the plot as a .html file.
                print("Saving: {}_{}_at_{}_black_and_white_separated_mutation_frequency_plots.html".format(dataset['name'],
                                                                                                                         variant['name'],
                                                                                                                         plotting_range['name']))
                                                                                                                         
                (plot_top & subplots_bottom).save('{}_{}_at_{}_black_and_white_separated_mutation_frequency_plots.html'.format(dataset['name'],
                                                                                                                         variant['name'],
                                                                                                                         plotting_range['name']))


def generate_dataset_comparison_plots(datasets, variants, frequency_ranks_data):
    """
    Generate the dataset comparison plots and save them as .html files.
    
    Parameters: datasets - the dictionary containing the dataset information
                variants - the dictionary containing the variant information
                frequency_ranks_data - the dictionary containing the frequency ranks data
    """
    
    # Set the plotting colors for the plotted attributes.
    category_colors = ['#984ea3', '#377eb8', '#4daf4a', '#e41a1c']
    
    # For each pair of datasets:
    for first_dataset in datasets.values():
        for second_dataset in datasets.values():
        
            # If the two datasets have different names:
            if first_dataset['name'] != second_dataset['name']:
            
                # For each variant:
                for variant in variants.values():
                    # Get the plotted attributes.
                    plotted_attributes = get_plotted_attributes(variant['name'])
                    
                    # Get the numbers of top frequency positions for both datasets. 
                    first_position_number = int(frequency_ranks_data[first_dataset['name']][variant['name']]['substitutions'].iloc[-1]['Frequency Rank'])
                    second_position_number = int(frequency_ranks_data[second_dataset['name']][variant['name']]['substitutions'].iloc[-1]['Frequency Rank'])
                    
                    # For each plotting range:
                    for plotting_range in [{'name':'Whole Gene','start':1, 'end':3822},
                                            {'name': 'First Subunit', 'start':1, 'end':1000},
                                            {'name':'Second Subunit', 'start':1000, 'end':2500},
                                            {'name':'Third Subunit', 'start':2500, 'end':3822}]:
                                            
                        # Get the required subsets.
                        first_subset = first_dataset['counts_freqs'].sort_values(by=['Substitution_Freq'], ascending=False).head(first_position_number).sort_values(by=['Nucleotide Position'])
                        second_subset = second_dataset['counts_freqs'].sort_values(by=['Substitution_Freq'], ascending=False).head(first_position_number).sort_values(by=['Nucleotide Position'])
                        first_plotted_subset = first_subset[(first_subset['Nucleotide Position'] >= plotting_range['start']) & (first_subset['Nucleotide Position'] <= plotting_range['end'])]
                        second_plotted_subset = second_subset[(second_subset['Nucleotide Position'] >= plotting_range['start']) & (second_subset['Nucleotide Position'] <= plotting_range['end'])]
                        
                        
                        # Generate the two plots.
                        first_dataset_plot = alt.Chart(first_plotted_subset).transform_fold(plotted_attributes
                        ).mark_bar(width=1, color='black').encode(
                            x =alt.X('Nucleotide Position', axis=alt.Axis(title='Nucleotide Positions of the S-gene', titleFontSize=14, labelFontSize=12), scale=alt.Scale(nice=False)),
                            y= alt.Y('value:Q', scale=alt.Scale(domain=[0,1]),axis=alt.Axis(title='Mutation Frequency',titleFontSize=14, labelFontSize=12)),
                            color=alt.Color('key:N', legend=alt.Legend(titleFontSize=14, labelFontSize=12, labelLimit=300), scale=alt.Scale(range=category_colors), title='Mutation Category'),
                            tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']).properties(
                            width=800,
                            height=150,
                            title={'text':'Subset of ' + first_dataset['name'],"fontSize":14,
                            #       'subtitle':'Index: 1000-2500', "subtitleFontSize":14
                            }
                        )

                        # Create the second hotspot plot for the new data, and combine the two plots.
                        second_dataset_plot = alt.Chart(second_plotted_subset).transform_fold(plotted_attributes
                        ).mark_bar(width=1, color='black').encode(
                            x =alt.X('Nucleotide Position', axis=alt.Axis(title='Nucleotide Positions of the S-gene', titleFontSize=14, labelFontSize=12), scale=alt.Scale(nice=False)),
                            y= alt.Y('value:Q', scale=alt.Scale(domain=[0,1]),axis=alt.Axis(title='Mutation Frequency',titleFontSize=14, labelFontSize=12)),
                            color=alt.Color('key:N', scale=alt.Scale(range=category_colors), title='Mutation Category'),
                            tooltip=['Nucleotide Position','Amino Acid Position:N','Substitution_Freq', 'Deletion_Freq']).properties(
                            width=800,
                            height=150,
                            title={'text':'Subset of '+ second_dataset['name'],"fontSize":14,
                            #       'subtitle':'Index: 1000-2500', "subtitleFontSize":14
                            }
                        )

                        # Save the .html file.
                        print("Saving: {}_vs_{}_{}_at_{}_comparison_mutation_frequency_plot.html".format(first_dataset['name'], 
                                                                                                         second_dataset['name'], 
                                                                                                         variant['name'],
                                                                                                         plotting_range['name']))

                        (first_dataset_plot & second_dataset_plot).save('{}_vs_{}_{}_at_{}_comparison_mutation_frequency_plot.html'.format(first_dataset['name'],
                                                                                                                                           second_dataset['name'],
                                                                                                                                           variant['name'],
                                                                                                                                           plotting_range['name']))

def print_high_frequency_substitution_or_deletion_positions(datasets):
    """
    Prints the positions with high frequency substitutions or deletions.
    
    Parameter: datasets - the dictionary containing the dataset information
    """
    
    # Disable the maximum number of columns shown.
    pd.set_option('display.max_columns', None)
    
    print("Printing high frequency positions:\n")
    
    # For each dataset:
    for dataset in datasets.values():
    
        # Get the position subset.
        position_subset = dataset['counts_freqs']
        
        # Subset for the positions with frequencies >= 0.1.
        high_frequency_positions = position_subset[(position_subset['Substitution_Freq'] >= 0.1) | (position_subset['Deletion_Freq'] >= 0.1)]
        
        # Print the high frequency positions.
        print("High Frequency Mutation Positions in {}:".format(dataset['name']))
        print(high_frequency_positions)
        print()

# If the user runs the file:    
if __name__ == '__main__':
    print("Output of general_variant_finder.py")
    print("Generated at {}.\n".format(datetime.datetime.now()))
    print("!Importing datasets.\n")
    datasets = import_counts_freqs_data()
    
    print("!Importing variant information.\n")
    variants = import_variant_data()
    
    print("!Printing the numbers of mutations in each dataset.\n")
    print_numbers_of_variant_mutations(variants)
    
    print("!Adding mutation classification attributes.\n")
    add_mutation_classification_attributes(datasets, variants)
    
    print("!Printing the variant counts in each dataset.\n")
    print_variant_counts_in_each_dataset(datasets, variants)
    
    print("Finding frequency ranks data.\n")
    frequency_ranks_data = find_variant_frequency_ranks_per_dataset(datasets, variants)
    
    print("!Plotting the substitution and deletion frequency rank plots for each dataset.\n")
    generate_frequency_rank_plots(datasets, variants, frequency_ranks_data)
    
    print("!Generating black and white mutation frequency plots.\n")
    generate_black_and_white_mutation_frequency_plots(datasets, variants, frequency_ranks_data)
    
    print("\n!Generating color dataset comparison plots.\n")
    generate_dataset_comparison_plots(datasets, variants, frequency_ranks_data)
    
    print("\n!Printing high frequency substitution or deletion positions.\n")
    print_high_frequency_substitution_or_deletion_positions(datasets)
    