#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Import the required libraries.
from Bio.Seq import Seq



def extract_sequences(maf_file):
    """Extracts the sequence strings from a .maf file
       Params: maf_file - the name of the .maf file
       
       Returns: reference - the reference genome sequence
                other - the other genome sequence"""
                
    # Extract the sequence lines from the .maf file.
    sequence_lines = [(line.split()[1], line.split()[2], line.split()[6]) for line in open('../uniqueSeqs.d/'+maf_file) if line.startswith('s')]
    
    # If sequences exists, extract the sequences, otherwise print the name of the file.
    try:
        reference = Seq(sequence_lines[0][2])
    except:
        print(maf_file)
        
    # Get the reference sequence's id.
    reference.id = sequence_lines[0][0]
    
    # Get the reference sequence's start location.
    reference.start = int(sequence_lines[0][1])
    
    
    #print(reference.start)
    
    # Get the other dna sequence.
    other = Seq(sequence_lines[1][2])
    
    # Get the other dna sequence's id.
    other.id = sequence_lines[1][0]
    
    # Get the other dna sequence's start location.
    other.start = int(sequence_lines[1][1])
    #print(other.id)
    
    # Return the reference and other sequences.
    return reference, other
#extract_sequences('../NC_045512.OD978514.maf')                      

