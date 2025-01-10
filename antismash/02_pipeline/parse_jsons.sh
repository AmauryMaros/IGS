#!/bin/bash

#SBATCH --job-name=jsons
#SBATCH --output=/local/scratch/amaros/antismash/logs/%x_%A_%a.out
#SBATCH --error=/local/scratch/amaros/antismash/logs/%x_%A_%a.err
#SBATCH --mem=64GB

cd /local/scratch/amaros/antismash/02_pipeline/

#/usr/local/packages/python-3.11/bin/python3 01_process_antismash_output.py /local/scratch/amaros/antismash/results_antismash/ /local/scratch/amaros/antismash/03_results/jsons/

/usr/local/packages/python-3.11/bin/python3 02_process_antismash_json.py /local/scratch/amaros/antismash/03_results/jsons/ /local/scratch/amaros/antismash/03_results/csv_files/


