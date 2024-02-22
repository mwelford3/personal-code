# Name: Michael A. Welford
# Filename: multi_deletion_counter.py Thesis Version
# Tool Name: Multi Mutation Counter
#
# Required input files:
# ... This needs to become a relative path.
# 
# Output file names:
# temp_multi_contiguous_deletion_counter.txt
# multi_deletion_counts_freq_for_S_all.csv
# multi_deletion_lengths_counts_freq_for_S_all.csv


# Import required libraries.
import re
from gene_reader import dna_reader

# The main function.
def main():

    # Initialize variables.
    reference = True
    lengths = {}
    sequence_number = 0
    ref_sequence = ''
    variant_sequence = ''
    
    
    # Initialize counts.
    contiguous_deletion_counts = [{} for i in range(3822)]
    deletion_length_counts = {}
    num_sequences_with_deletions = 0
    
    
    # Import the gene information.
    genes = dna_reader()
    
    
    # For each line in the multi alignment .txt file:
    # If the line starts with 's':
    for line in (line for line in open('/mnt/home/z1679714/sars-cov2-GISAID-Sgene/test13.above97.txt') if line.startswith('s')):
        
        # Split the line into tokens.
        line_tokens = re.split('\s+', line.rstrip())

        # If it corresponds to a reference sequence:
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
                with open('temp_multi_contiguous_deletion_counter.txt', 'w') as temp_file:
                    temp_file.write(str(sequence_number) + '\n')
                print(sequence_number)
                
               
            # Get the relevant sequence information for the other/variant sequence.
            other_group_id = int(line_tokens[1])
            line_otherstart = int(line_tokens[2])
            line_otherlength = int(line_tokens[3])
            other_sequence = line_tokens[-1]
            othersequence_length = len(other_sequence)
                
            # Remove insertions 
            ref_sequence, other_sequence = fix_sequences(ref_sequence, other_sequence)
            
            # If the other/variant sequence contains a '-':
            if '-' in other_sequence:
                # Increment the number of sequences with deletions.
                num_sequences_with_deletions += 1
                
            # Count the contiguous deletions.
            count_contiguous_deletions(ref_sequence, other_sequence, contiguous_deletion_counts, deletion_length_counts)

            # Set the reference tag to true since a reference sequence will be read next.            
            reference = True
    
    # Print the deletion counts dictionary.    
    print(contiguous_deletion_counts)
    
    # Print the number of sequences with deletions.
    print(num_sequences_with_deletions)
    
    # Write the contiguous deletion counts to a .csv file.
    contiguous_deletion_counts_to_file(contiguous_deletion_counts, sequence_number, num_sequences_with_deletions)
    
    # Write the deletion length data to a .csv file.
    deletion_lengths_to_file(deletion_length_counts, sequence_number)

def count_contiguous_deletions(reference, other, contiguous_deletion_counts, deletion_length_counts):
    """
    Counts the numbers of contiguous deletions (continuous strings of '-'s).
    
    Parameters: reference - the reference gene sequence
                other     - the other/variant gene sequence
                contiguous_deletion_counts - the dictionary containing the contiguous deletion counts
                deletion_length_counts - the dictionary containing the deletion length data
    """
    
    # Initialize the deletion length and temp length counts dictionary.
    deletion_length = 0
    temp_length_counts = {}
    
    # For each nucleotide index.
    for nucleotide_index in range(len(other)):
    
        # Get the nucleotide in the other/variant sequence.
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
    Writes the contiguous (continuous string of '-'s) deletion data to an output file.
    
    Parameters: contiguous_deletion_counts - the dictionary with the contiguous deletion information
                sequence_number - the number of sequences read
                num_sequences_with_deletions - the number of sequences with deletions
    """
    
    # Print the number of sequences and the number of sequences with deletions.
    print("Sequence Number: {}".format(sequence_number))
    print("Number of Sequences with Deletions:",num_sequences_with_deletions)
    
    
    # Open the new counts file.
    counts_file = open('multi_deletion_counts_freq_for_S_all.csv', 'w')

    # Write the column names for the .csv file.
    counts_file.write('Starting_Nucleotide_Position,Deletion_Length,Ending_Nucleotide_Position,Deletion_Count,Deletion_Freq,Num_Sequences_With_Deletions,Ratio_With_Deletions\n')
    
    # For each index value.
    for i in range(3822):
        # Get the nucleotide position.
        nucleotide_position = i + 1
        
        # For each deletion length:
        for deletion_length in sorted(contiguous_deletion_counts[i].keys()):
            # Calculate the ending position.
            ending_position = nucleotide_position + deletion_length - 1
               
            # Get the deletion count.
            deletion_length_count = contiguous_deletion_counts[i][deletion_length]
            
            # Calculate the frequency.
            deletion_length_freq = deletion_length_count / sequence_number
            
            # Calculate the frequency of sequences with deletions.
            ratio_with_deletions = num_sequences_with_deletions / sequence_number 
            
            # Write the line in the output file.
            counts_file.write('{},{},{},{},{},{},{}\n'.format(nucleotide_position, deletion_length, ending_position, deletion_length_count, deletion_length_freq,num_sequences_with_deletions, ratio_with_deletions))

    # Close the counts file.
    counts_file.close()

def deletion_lengths_to_file(deletion_length_counts, sequence_number):
    """
    Writes the deletion lengths, counts, and frequencies to a output file.
    
    Parameters: deletion_length_counts - the dictionary containing the numbers of deletions of each length
                sequence_number - the number of sequences read 
    """
    
    # Open the output file for the deletion length data.
    lengths_file = open('multi_deletion_lengths_counts_freq_for_S_all.csv', 'w')
    
    # Write the header.
    lengths_file.write('Deletion Length,Count,Frequency\n')
    
    # For each deletion length:
    for length in sorted(deletion_length_counts.keys()):
    
        # Get the count of deletions of that length.
        deletion_length_count = deletion_length_counts[length]
        
        # Calculate the frequency.
        deletion_length_freq = deletion_length_count / sequence_number
        
        # Write the line with the data.
        lengths_file.write('{},{},{}\n'.format(length, deletion_length_count, deletion_length_freq))
        
    # Close the file.
    lengths_file.close()

        
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
        print("The length of the sequences is not 3822.")
        exit()
        
        
# Run the main function.        
if __name__ == '__main__':
    main()
