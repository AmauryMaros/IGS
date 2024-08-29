#!/bin/bash

#######################################
# Set parameters
#######################################

#$ -cwd -V              # Use the current working directory and inherit current environment variables
#$ -l mem_free=16G      # Set memory requirement
#$ -P project_name      # Specify project name
#$ -q all.q             # Select queue
#$ -N job_name          # Name of the job
#$ -j y                 # Join stdout and stderr
#$ -o path/to/logs      # set the log file location for stdout
#$ -e path/to/logs      # set the log file location for stderr
#$ -t 1-10              # Define an array job with tasks 1 to 10

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

infile=`sed -n "$SGE_TASK_ID p" list_of_samples.txt`

# Run the script
Rscript path/to/Rscript.R
