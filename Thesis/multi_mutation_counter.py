# Name: Michael A. Welford
# Filename: multi_mutation_counter.py Thesis Version
# Tool Name: Multi Mutation Counter
#
# Required input files:
# /mnt/home/z1679714/sars-cov2-GISAID-Sgene/test13.above97.txt This needs to become a relative path.
# 
# Output file names:
# new_mutation_counts_freq_for_S_all.csv


# Import required libraries.
import pickle
import numpy as np
import pandas as pd
import re
from gene_reader import dna_reader
from sys import argv

# The main function.
def main():

    # Initialize variables.
    reference = True
    lengths = {}
    sequence_number = 0
    ref_sequence = ''
    other_sequence = ''
    
    
    # Initialize counts.
    mutation_counts = [ {} for i in range(3822)]
    deletion_counts = [ 0 for i in range(3822)]
    
    for i in range(len(mutation_counts)):
        for nuc in ('A', 'T', 'G', 'C', '-'):
            mutation_counts[i][nuc] = {'Count': 0, 'Groups': []}


    # Import the gene information.
    genes = dna_reader()
    
    # Print the number of genes and the length of the reference S-gene sequence.
    print(genes)
    print(len(genes[3]['sequence']))

    # For each line in the multi alignment .txt file:
    # If the line starts with 's':
    for line in (line for line in open('/mnt/home/z1679714/sars-cov2-GISAID-Sgene/test13.above97.txt') if line.startswith('s')):
        
        # Split the line into tokens.
        line_tokens = re.split('\s+', line.rstrip())

        # If it corresponds to a reference genome:
        if reference:
            # Get the reference starting position, reference length, and reference sequence.
            line_refstart = int(line_tokens[2])
            line_reflength = int(line_tokens[3])
            ref_sequence = line_tokens[-1]

            # Find the reference sequence length.
            refsequence_length = len(ref_sequence)
            
            # Set the reference tag to false since a reference line has been read.
            reference = False

        # Otherwise, the sequence is a variant:
        else:
            # Increment the number of sequences read.
            sequence_number += 1
            
            # For every 1000 sequences read, print the current sequence number to the temp_file and stdout.
            if sequence_number % 1000 == 0:
                with open('temp_new_mutation_counter.txt', 'w') as temp_file:
                    temp_file.write(str(sequence_number) + '\n')
                print(sequence_number)
                
                
            # Get the relevant sequence information for the other/variant sequence.
            other_group_id = int(line_tokens[1])
            line_otherstart = int(line_tokens[2])
            line_otherlength = int(line_tokens[3])
            other_sequence = line_tokens[-1]
            othersequence_length = len(other_sequence)
            
            
            # Use the fix sequences method to remove insertion columns.
            ref_sequence, other_sequence = fix_sequences(ref_sequence, other_sequence)
            
            # Use the compare_sequences to compare the reference and other/variant sequences.
            compare_sequences(ref_sequence, other_sequence, mutation_counts, other_group_id)
            
            # Set the reference tag to true since a reference sequence will be read next.
            reference = True


    # Print the mutation counts dictionary.
    print(mutation_counts)
    
    # Fill the deletion counts dictionary.
    fill_deletion_counts(mutation_counts, deletion_counts)
    
    # Simplify the counts dictionary by removing empty inner dictionaries.
    simplify_counts_dict(mutation_counts)
    
    # Convert the counts to the parsable file.
    #convert_to_parse_file(mutation_counts)
    
    # Save the counts as a pickle binary file.
    save_pickle(mutation_counts)
    
    # Save the counts/frequencies to an output file.
    counts_to_file(mutation_counts, deletion_counts, sequence_number)

def fill_deletion_counts(mutation_counts, deletion_counts):
    """
    Fills the deletion counts dictionary with the deletion values from the mutation_counts dictionary.
    """
    for i in range(len(mutation_counts)):
        deletion_counts[i] = mutation_counts[i]['-']['Count']

def save_pickle(mutation_counts):
    """
    Saves the mutation_counts dictionary as a pkl file.
    """
    pickle_file = open('test13_above97_mutation_counts.pkl', 'wb')
    pickle.dump(mutation_counts, pickle_file)

def compare_sequences(reference, other, mutation_counts, group_id):
    """
    Increments the mutation_counts dictionary for the mutations between a reference sequence and
    an other/variant sequence.
    
    Parameters: reference - the reference sequence string being compared
                other - the other/variant sequence string being compared
                mutation_counts - the dictionary containing the mutation counts
                group_id - the group_id for the sequence pair
    """

    # For each nucleotide position in the reference sequence,
    for i in range(len(reference)):
        # If a substitution or deletion is found:
        if reference[i] in 'ATCG' and other[i] in 'ATCG-':
            if reference[i] != other[i]:
                # Increment the mutation counts at the position and append the groups subdictionary.
                mutation_counts[i][other[i]]['Count'] += 1
                mutation_counts[i][other[i]]['Groups'].append(group_id)

def simplify_counts_dict(mutation_counts):
    """
    Simplifies the mutation_counts dictionary by removing empty subdictionaries.
    
    Parameter: mutation_counts - the dictionary containing the mutation counts
    """
    
    # For each position in the mutation counts dictionary:
    for i in range(len(mutation_counts)):
        # For each type of nucleotide character (ATCG-):
        for nuc in list(mutation_counts[i].keys()):
        
            # If the subdictionary is empty, pop it.
            if len(mutation_counts[i][nuc]['Groups']) == 0:
                mutation_counts[i].pop(nuc)

def convert_to_parse_file(mutation_counts):
    """
    Write a parsable file with the full substitution information.
    This includes the resulting nucleotide.
    
    # Parameter: mutation_counts - the dictionary containing the mutation counts.
    """
    
    # Open the output parse file:
    with open('test13.above97.substitution.unique.sites.txt', 'w') as parse_file:

        # For each position in the mutation_counts dictionary:
        for i in range(len(mutation_counts)):
            # If the position has substitutions:
            if len(mutation_counts[i]) > 0:
                # Write the position the number of substitutions.
                parse_file.write('{} : {} : '.format(i, len(mutation_counts[i])))
                
                # For each nucleotide type:
                for nuc in sorted(mutation_counts[i].keys()):
                
                    # Check that the number of mutations is correct.
                    assert mutation_counts[i][nuc]['Count'] == len(mutation_counts[i][nuc]['Groups'])
                    
                    # Write the nucleotide character and the mutation count.
                    parse_file.write('< {} : {} : '.format(nuc, mutation_counts[i][nuc]['Count']))
                    
                    # Write the groups.
                    for group in sorted(mutation_counts[i][nuc]['Groups']):
                        parse_file.write('{} '.format(group))
                    parse_file.write('> ')
                    
                # End the line.
                parse_file.write('\n')


def counts_to_file(mutation_counts, deletion_counts, sequence_number):
    """
    Writes the substitution and deletion counts and frequencies to the output file.
    
    Parameters: mutation_counts - the dictionary containing the mutation counts
                deletion_counts - the dictionary containing the deletion counts
                sequence_number - the variable containing the total number of sequences
    """
    
    # Print the number of sequences.
    print("Sequences Number: {}".format(sequence_number))
    
    # Open the new counts file.
    counts_file = open('new_mutation_counts_freq_for_S_all.csv', 'w')

    # Write the column names for the .csv file.
    counts_file.write('Index,Substitution_Count,Deletion_Count,Substitution_Freq,Deletion_Freq\n')

    # For each index position in the sequence:
    for i in range(len(mutation_counts)):
        # Write the index and mutation count to the file.
        substitution_count = 0
        for nuc in ('A','T','C','G'):
            if nuc in mutation_counts[i].keys():
                substitution_count += mutation_counts[i][nuc]['Count']
            else:
                substitution_count += 0

        # Calculate the substitution frequency.
        substitution_freq = substitution_count/sequence_number
        
        # Get the deletion count.
        if '-' in mutation_counts[i].keys():
            deletion_count = mutation_counts[i]['-']['Count']
        else:
            deletion_count = 0
            
        # Calculate the deletion frequency.
        deletion_freq = deletion_count/sequence_number

        # Write the corresponding line in the output .csv file.
        counts_file.write('{},{},{},{},{}\n'.format(i,substitution_count,deletion_count,substitution_freq,deletion_freq))

    # Close the counts file.
    counts_file.close()
        
def fix_sequences(reference, other):
    """
    Removes columns from sequences for insertions.
    
    Parameters: reference - the reference sequence
                other     - the other/variant sequence
                
    Returns:    new_ref   - the updated reference sequence
                new_other - the updated other/variant sequence
    """
    
    # Initialize the new sequences.
    new_ref = ''
    new_other = ''
    
    # For each position in the reference sequence:
    for i in range(len(reference)):
        # If an insertion is found, skip it.
        if reference[i] == '-':
            pass
        # Otherwise append the characters.
        else:
            new_ref += reference[i]
            new_other += other[i]

    # Make sure the lengths are correct.
    # Otherwise stop and print a message.
    if len(new_ref) == len(new_other) and len(new_ref) == 3822:
        return new_ref, new_other
    else:
        print("Sequences were not the correct length. (3822)")
        exit()
        
# Run the main function.
if __name__ == '__main__':
    main()
