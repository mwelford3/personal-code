# Name: Michael A. Welford
# Filename: pairwise_deletion_counter.py Thesis Version
# Tool Name: Pairwise Deletion Counter
#
# Required input files:
# 1. unique sequences in '../uniqueSeqs.d/pw.d/'
# 2. bad_files.out
# 
# 
# Output file names:
#     pairwise_deletion_counts_freq_for_S_all.csv
#     pairwise_deletion_lengths_counts_freq_for_S_all.csv
#

# Import required libraries/packages.
from sys import argv
from os import listdir
from maf_reader import extract_sequences
from gene_reader import dna_reader
import numpy as np
import pandas as pd
from sequence_comparer import compare_dna_sequences

# The main function.
def main():
   
    # Get the total number of unique sequences.
    MAX_NUMBER = sum(1 for file in listdir('../uniqueSeqs.d/pws.d/'))
    
    # Import the gene information.
    genes = dna_reader()
    
    # Initialize the contiguous_deletion_counts list.
    contiguous_deletion_counts = [{} for i in range(3822)]
    
    # Initialize the number of files.
    file_number = 0
    
    # Input the list of files missing sequences.
    bad_files = list(line.rstrip() for line in open('bad_files.out'))
    
    # Initialize the deletion length counts dictionary.
    deletion_length_counts = {}
    
    # Initialize the number of sequences with deletions.
    num_sequences_with_deletions = 0
    
    # For each valid maf file:
    for maf_file in (file for file in listdir('../uniqueSeqs.d/pws.d/') if (file not in bad_files)):
        # Increment the number of files.
        file_number += 1
        
        # Write the number of files read for every 1000 sequences.
        if file_number % 1000 == 0:
            with open('old_deletion_temp.txt', 'w') as temp_file:
                print(file_number, file=temp_file)
            print("Files Read: {}".format(file_number))
            
        
        # Split the name of the maf file into tokens.
        tokens = maf_file.split('.')
        
        # Extract the reference and other/variant sequences from the maf file. 
        reference_sequence, other_sequence = extract_sequences(maf_file)
        
        # For the S-gene, splice out the S-gene sequences from the whole genome sequences.
        for protein_number in [3]:
            protein_name = genes[protein_number]['protein_name']
            locations = genes[protein_number]['location']
            
            ref_gene_sequence = reference_sequence[locations[0]+-1-reference_sequence.start:locations[1]-reference_sequence.start]
            other_gene_sequence = other_sequence[locations[0]+-1-reference_sequence.start:locations[1]-reference_sequence.start]
            
        # Count the numbers of contiguous (strings of '-'s) deletions in the compared sequences.
        count_contiguous_deletions(ref_gene_sequence, other_gene_sequence, contiguous_deletion_counts, deletion_length_counts)
    
    # Print the file contiguous deletion counts dictionary.    
    print(contiguous_deletion_counts)
    
    # Write the final file number and contiguous deletion counts to the temp file.
    with open('old_deletion_temp.txt', 'a') as temp_file:
        print(file_number, file=temp_file)
        print(contiguous_deletion_counts, file=temp_file)
    
    # Write the contiguous deletion counts to a .csv file.    
    contiguous_deletion_counts_to_file(contiguous_deletion_counts, file_number,num_sequences_with_deletions)
    
    # Write the deletion length data to a .csv file.
    deletion_lengths_to_file(deletion_length_counts, file_number)    
        
        
def count_contiguous_deletions(reference, other, contiguous_deletion_counts, deletion_length_counts):
    """
    Counts the numbers of contiguous (continuous strings of '-'s) deletions between two sequences.
    
    Parameters: reference - the reference sequence string
                other     - the other/variant sequence string
                contiguous_deletion_counts - the container of contiguous deletion counts
                deletion_length_counts - the dictionary containing the numbers of deletions of each given length
    """
    
    # Initialize the deletion length variable.
    deletion_length = 0
    
    # Initialize the temporary length counts dictionary.
    temp_length_counts = {}
    
    # For each nucleotide index/position in the other/variant sequence:
    for nucleotide_index in range(len(other)):
        # Get the nucleotide character.
        nucleotide = other[nucleotide_index]
        
        # If it is a '-', increment the deletion length.
        if nucleotide == '-':
            deletion_length += 1
        
        # Otherwise, it is either the character is before a deletion or after a deletion:
        else:
            # If the character is after a deletion (i.e. current deletion length is not 0):
            if deletion_length != 0:
                # Add the starting position, and deletion length to the dictionary.
                contiguous_deletion_counts[nucleotide_index - deletion_length][deletion_length] = contiguous_deletion_counts[nucleotide_index - deletion_length].get(deletion_length, 0) + 1
                
                # Increment the deletion length count by 1.
                temp_length_counts[deletion_length] = temp_length_counts.get(deletion_length, 0) + 1
                
                # Reset the deletion length to 0.
                deletion_length = 0
            # Otherwise continue the deletion.
            else:
                continue
    # Increment the deletion length counts for all new deletions.
    for deletion_length in temp_length_counts.keys():
        deletion_length_counts[deletion_length] = deletion_length_counts.get(deletion_length, 0) + 1
    
   
def contiguous_deletion_counts_to_file(contiguous_deletion_counts, sequence_number, num_sequences_with_deletions):
    """
    Saves the deletion counts to a .csv file.
    
    Parameters: contiguous_deletion_counts - the dictionary containing the deletion counts
                sequence_number - the total number of sequences
                num_sequences_with_deletions - the number of sequences with deletions
    """
    
    # Print the number of sequences.
    print("Sequence Number: {}".format(sequence_number))
    
    # Open the new counts file.
    counts_file = open('pairwise_deletion_counts_freq_for_S_all.csv', 'w')

    # Write the column names for the .csv file.
    counts_file.write('Starting_Nucleotide_Position,Deletion_Length,Ending_Nucleotide_Position,Deletion_Count,Deletion_Freq,Num_Sequences_With_Deletions,Ratio_With_Deletions\n')

    # For each index value:
    for i in range(3822):
    
        # Get the nucleotide position.
        nucleotide_position = i + 1
        
        # For each deletion length:
        for deletion_length in sorted(contiguous_deletion_counts[i].keys()):
        
            # Calculate the ending position.
            ending_position = nucleotide_position + deletion_length - 1
            
            # Get the deletion length count.
            deletion_length_count = contiguous_deletion_counts[i][deletion_length]
        
            # Calculate the frequency.
            deletion_length_freq = deletion_length_count / sequence_number
            
            # Get the percentage of sequences with deletions.
            ratio_with_deletions = num_sequences_with_deletions / sequence_number
            
            # Write the line in the output file.
            counts_file.write('{},{},{},{},{},{},{}\n'.format(nucleotide_position, deletion_length, ending_position, deletion_length_count, deletion_length_freq, num_sequences_with_deletions, ratio_with_deletions))

    # Close the counts file.
    counts_file.close()

def deletion_lengths_to_file(deletion_length_counts, sequence_number):
    """
    Writes the (deletion length, frequency) data to a .csv file.

    Parameters: deletion_length_counts - the dictionary containing the deletion lengths
                sequence_number - the number of sequences    
    """
    
    # Open the output file.
    lengths_file = open('pairwise_deletion_lengths_counts_freq_for_S_all.csv', 'w')
    
    # Write the column names for the output file.
    lengths_file.write('Deletion Length,Count,Frequency\n')
    
    # For each deletion length:
    for length in sorted(deletion_length_counts.keys()):
    
        # Get the count of deletions with the given length.
        deletion_length_count = deletion_length_counts[length]
        
        # Calculate the frequency.
        deletion_length_freq = deletion_length_count / sequence_number
        
        # Write the line in the output file.
        lengths_file.write('{},{},{}\n'.format(length, deletion_length_count, deletion_length_freq))
        
    # Close the file.
    lengths_file.close()

        
# Runs the count_mutations function and times the execution.
if __name__ == '__main__':
    main()
