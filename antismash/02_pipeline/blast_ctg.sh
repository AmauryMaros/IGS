#!/bin/bash

#SBATCH --job-name=blast_ctg
#SBATCH --output=/local/scratch/amaros/antismash/logs/%x_%A_%a.out
#SBATCH --error=/local/scratch/amaros/antismash/logs/%x_%A_%a.err
#SBATCH --mem=32GB

cd /local/scratch/amaros/antismash/02_pipeline/

/usr/local/packages/python-3.11/bin/python3 05_blast_ctg.py
