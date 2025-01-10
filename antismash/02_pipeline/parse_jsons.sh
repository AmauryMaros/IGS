#!/bin/bash

#SBATCH --job-name=jsons
#SBATCH --output=/local/scratch/amaros/antismash/logs/%x_%A_%a.out
#SBATCH --error=/local/scratch/amaros/antismash/logs/%x_%A_%a.err
#SBATCH --mem=64GB

cd /local/scratch/amaros/antismash/02_pipeline/

# Filter JSON with/without results
/usr/local/packages/python-3.11/bin/python3 01_process_antismash_output.py /local/scratch/amaros/antismash/results_antismash/ /local/scratch/amaros/antismash/03_results/jsons/

# Parse JSON
# /usr/local/packages/python-3.11/bin/python3 02_process_antismash_json.py /local/scratch/amaros/antismash/03_results/jsons/ /local/scratch/amaros/antismash/03_results/csv_files/

# Python scripts
# /usr/local/packages/python-3.11/bin/python3 03_get_ctg_coordinates.py
# /usr/local/packages/python-3.11/bin/python3 04_get_ctg_sequences.py
# /usr/local/packages/python-3.11/bin/python3 05_blast_ctg.py

