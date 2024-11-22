from Bio import SeqIO
import pandas as pd
import os

# Read the genes positions CSV
genes_positions = pd.read_csv("../03_results/antiSMASH_geneID_w_coordinates.csv")

# Define input and output paths
output_file = "my_output.fasta"
input_file = "directory/with/fasta_files/"

with open(output_file, "w") as out_f:
    # Loop through each unique MAG
    for i in genes_positions['MAG'].unique():
        fasta_file = f"{input_file}/{i}.fasta"
        
        # Check if the FASTA file exists
        if not os.path.exists(fasta_file):
            print(f"FASTA file {fasta_file} not found, skipping...")
            continue
        
        # Get the target sequence IDs for this MAG
        target_ids = genes_positions[genes_positions['MAG'] == mag_id]['sequence'].unique()
        
        # Parse the FASTA file and extract matching sequences
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id in target_ids:  # Check if the sequence ID matches
                SeqIO.write(record, out_f, "fasta")
                print(f"Sequence {record.id} written to {output_file}")
    
    print("All sequences copied.")
