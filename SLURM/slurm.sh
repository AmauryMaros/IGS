#!/bin/bash

#######################################
# Set parameters
#######################################

#SBATCH --job-name=job_name                 # Name of the job
#SBATCH --output=path/to/logs/%x_%A_%a.out  # Standard output log (%x is job name, %A is job ID, %a is array task ID)
#SBATCH --error=path/to/logs/%x_%A_%a.err   # Standard error log (%x is job name, %A is job ID, %a is array task ID)
#SBATCH --ntasks=1                          # Run on a single task
#SBATCH --cpus-per-task=8                   # Number of CPU cores per task
#SBATCH --mem=16G                           # Memory per node
#SBATCH --array=1-10                        # Array job
#SBATCH --partition=general                 # Specify the partition (general queue)

#######################################
# Conda activation
#######################################

source /usr/local/packages/miniconda3/etc/profile.d/conda.sh
conda activate /path/to/conda/env

#######################################
# Script execution
#######################################

# Go to working directory
cd /path/to/working/directory

infile=$(sed -n "${SLURM_ARRAY_TASK_ID}p" list_of_samples.txt)

# Run the script
Rscript path/to/Rscript.R  --cpus $SLURM_CPUS_PER_TASK
