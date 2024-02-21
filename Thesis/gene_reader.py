# Import required libraries.
from Bio import SeqIO
from Bio.Seq import Seq
import pandas as pd
import re
from maf_reader import extract_sequences

# Reads the coding gene information from the annotations file.
#
# Returns: genes - a dictionary with the gene information
def dna_reader():

    # Open the annotations file.
    dna_annotations_file = open('../sars2variants/annotations/NC_045512.2.codingDNA.txt')
    
    # Initialize an empty genes dictionary.
    genes = {}
    
    # Initalize the counter for the number of genes.
    gene_number = 0
    
    # For each line in the annotations file:
    for line in dna_annotations_file:

        # If the line starts with '>':
        if line.startswith('>'):
        
            # Increment the gene number.
            gene_number += 1
            
            # Split the line to get the gene information
            gene_info = line.split()
            
            # Extract the gene name.
            gene_name = gene_info[1]
            
            # Extract the protein name.
            protein_name = gene_info[4] +', '+ gene_info[5]
            
            # Initalize the inner dictionary for the specific gene.
            genes[gene_number] = {}
            
            # Set the gene name.
            genes[gene_number]['gene_name'] = gene_name
            
            # Set the protein name.
            genes[gene_number]['protein_name'] = protein_name
            
            # Print the information.
            print(gene_info)
            print(gene_name)
            print(protein_name)
            
            # If the location contains a union:
            if 'join' in line:
            
                # Use a regular expression to get the location infomation.
                location_pattern = '(\d+)\.\.(\d+),(\d+)\.\.(\d+)'
                location_match = re.search(location_pattern, line)
                locations = ((int(location_match.group(1)), int(location_match.group(2))), 
                            (int(location_match.group(3)), int(location_match.group(4))))
                            
                            
                # Set the location in the dictionary.
                genes[gene_number]['location'] = locations
                
                # Print the locations
                print(locations)
                
            # Otherwise: 
            else:
                # Use a regular expression to get the location information.
                location_pattern = 'location=(\d+)\.\.(\d+)'
                location_match = re.search(location_pattern, line)
                location_start = int(location_match.group(1))
                location_end = int(location_match.group(2))
                
                # Set the gene location.
                genes[gene_number]['location']=(location_start, location_end)
                
                # Print the location.
                print(location_start, location_end)
                
            # Initalize the sequence in the dictionary.
            genes[gene_number]['sequence'] = ''
            print()
            
        # Othewise append the line to the sequence.
        else:
            genes[gene_number]['sequence'] += line.rstrip()
            
    # Close the annotations file.
    dna_annotations_file.close()
    
    # Print the genes dictionary.
    print(genes)
    
    # Save the genes file to a csv.
    genes_df = pd.DataFrame(genes)
    genes_df.to_csv('genes.csv')
    
    return genes
    
    
# Reads the protein information from the protein annotations file.
def protein_reader():

    # Open the protein annotations file.
    protein_annotations_file = open('../sars2variants/annotations/NC_045512.2.codingProtein.txt')
    
    # Initialize a list for the protein sequences.
    protein_sequences = ['']
    
    # For each line in the protein annotations file:
    for line in protein_annotations_file:
    
        # If the line starts with '>':
        if line.startswith('>'):
            # Append the sequence.
            protein_sequences.append('')
        # Otherwise append the line to the last sequence in the list.
        else:
            protein_sequences[-1] += line.rstrip()
            
    # Returns the protein_sequences list.
    return protein_sequences

# Run the program.
if __name__ == '__main__':

    # Read the dna sequences.
    genes = dna_reader()
    
    # Read the protein sequences.
    protein_sequences = protein_reader()

    # Make sure the translated dna sequence matches the corresponding protein sequence.
    for gene_number in genes:
        #print(str(Seq(genes[gene_number]['sequence']).translate()))
        print(str(Seq(genes[gene_number]['sequence']).translate()[:-1]) == protein_sequences[gene_number])

    reference, _ = extract_sequences('NC_045512.MW865463.maf')
    print()
    #print(reference)
    
    
    # Make sure the gene sequences match correctly.
    for gene_number in range(1,13):
        if type(genes[gene_number]['location'][0]) == type(tuple()):
            locations = genes[gene_number]['location']
            print(locations)
            print(len(reference[locations[0][0]+-1:locations[1][1]]))
            print(len(genes[gene_number]['sequence']))
            print(reference[locations[0][0]-1-reference.start:locations[0][1]-reference.start] + reference[locations[1][0]-1-reference.start:locations[1][1]-reference.start] == genes[gene_number]['sequence'])
        #print(reference[genes[gene_number]['location'][0]+-1:genes[gene_number]['location'][1]])
        #print(genes[gene_number]['sequence'])
        else:
            print('Gene: {} ='.format(gene_number),reference[genes[gene_number]['location'][0]+-1-reference.start
                   :genes[gene_number]['location'][1]-reference.start] == genes[gene_number]['sequence'])
            #print(len(reference[genes[gene_number]['location'][0]+-1+reference.start:genes[gene_number]['location'][1]+reference.start]))
            print(len(reference) - reference.find(genes[gene_number]['sequence']))
            print(genes[gene_number]['location'][0]+-1)
