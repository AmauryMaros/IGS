import subprocess

# Define paths
#input_fasta = "/local/scratch/amaros/antismash/03_results/antismash_genes_sequences2.fasta"
#blast_db = "/local/scratch/mfrance/VIRGO2/15_blastdb/Genes/VIRGO2"  
#output_file = "/local/scratch/amaros/antismash/03_results/blast_results2.txt"

input_fasta = "/local/scratch/mfrance/VIRGO2/12_package/VIRGO2.fa"
output_file = "/local/scratch/amaros/antismash/03_results/VIRGO2_vs_antismash_DB_nucl.txt"
blast_db = "/local/scratch/amaros/antismash/05_blast_DB/antismash_blast_db_nucl/antimsash_make_db_nucl"

# BLAST command
blast_command = [
    "blastn",  # Use "blastp" for protein sequences
    "-query", input_fasta,  # Input FASTA file
    "-db", blast_db,  # BLAST database
    "-out", output_file,  # Output file
    "-outfmt", "6",  # Output format (tabular)
    "-evalue", "1e-5",  # E-value threshold
    "-num_threads", "4"  # Number of threads for parallelization
]

# Run BLAST
try:
    subprocess.run(blast_command, check=True)
    print(f"BLAST completed successfully. Results saved to {output_file}")
except subprocess.CalledProcessError as e:
    print("BLAST command failed.")
    print(e)

