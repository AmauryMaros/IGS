from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pandas as pd

genes_position = pd.read_csv("../03_results/antiSMASH_geneID_w_coordinates2.csv")

# Create header
new_header = (
    genes_position['sequence'] + "/" +
    genes_position['ctg'] + "/" +
    genes_position['Start'].astype(str) + "/" +
    genes_position['End'].astype(str) + "/" +
    genes_position['Strand']
)

new_header = new_header.to_list()

# List to store all SeqRecord objects
all_records = []

# Process each entry in new_header
for elt in new_header:
    mag = elt.split("/")[0][:8]
    sequence_index = int(elt.split("/")[0].split("_")[-1])  # Extract sequence index
    start = int(elt.split("/")[2])
    end = int(elt.split("/")[3])
    strand = elt.split("/")[4]

    # File and sequence details
    #fasta_file = f"../00_test/{mag}.fasta"
    fasta_file = f"/local/projects-t3/LSVF/VIRGO2/final_bins/{mag}.fasta"
    
    # Parse the FASTA file
    with open(fasta_file, "r") as file:
        sequences = list(SeqIO.parse(file, "fasta"))

    # Ensure the requested sequence index is valid
    if sequence_index <= 0 or sequence_index > len(sequences):
        raise ValueError(f"Invalid sequence index: {sequence_index}. Total sequences: {len(sequences)}")

    # Extract the sequence (1-based index)
    target_sequence = sequences[sequence_index - 1]  # Adjust for 0-based indexing
    subsequence = target_sequence.seq[start - 1:end]  # Extract the region (1-based indexing)

    # Check strand direction
    if strand == "-":
        subsequence = subsequence.reverse_complement()

    # Create a SeqRecord for the FASTA entry
    record = SeqRecord(
        Seq(str(subsequence)),
        id=elt,  # Use `elt` as the FASTA header
        description=""  # Leave the description empty
    )
    all_records.append(record)

# Write all sequences to a single FASTA file
output_fasta = "../03_results/antismash_genes_sequences2.fasta"
with open(output_fasta, "w") as output_file:
    SeqIO.write(all_records, output_file, "fasta")

print(f"Combined FASTA file created: {output_fasta}")

