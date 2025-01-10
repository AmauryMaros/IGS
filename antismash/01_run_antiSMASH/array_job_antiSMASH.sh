#!/bin/bash

#SBATCH --job-name=antismash
#SBATCH --output=/local/scratch/amaros/antismash/01_run_antiSMASH/logs/%x_%A_%a.out
#SBATCH --error=/local/scratch/amaros/antismash/01_run_antiSMASH/logs/%x_%A_%a.err
#SBATCH --array=1-1500
#SBATCH --mem-per-cpu=40G
#SBATCH --cpus-per-task=4

# Conda activation
source /usr/local/packages/miniconda3/etc/profile.d/conda.sh
conda activate /usr/local/packages/miniconda3/envs/antismash

# Go to working directory
cd /local/scratch/amaros/antismash/01_run_antiSMASH/

infile=$(sed -n "${SLURM_ARRAY_TASK_ID}p" MAGs_list/mag_1_1500.txt)

# Run Antismash
/usr/local/packages/miniconda3/envs/antismash/bin/antismash \
  --cpus 4 \
  /local/projects-t3/LSVF/VIRGO2/final_bins/${infile}.fasta \
  --output-dir /local/scratch/amaros/antismash/results_antismash/${infile}/ \
  --genefinding-tool prodigal \
  --cb-general --cb-subclusters --cb-knownclusters --fullhmmer \
  --clusterhmmer --tigrfam --asf --cc-mibig --pfam2go --rre --smcog-trees
