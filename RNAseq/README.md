# RNA Seq pipeline

## Create conda envs with required packages
```bash
conda create -n RNAseq_env
conda activate RNAseq_env
conda install -c bioconda fastqc trimmomatic subread samtools
```
Install hisat2 with brew or conda
```bash
brew install hisat2
conda install -c bioconda
```

## Create architecture
```bash
# Update the path for raw data then run
./01_make_architecture.sh
```

## Process the raw data
```bash
# If few samples
./02_runRNASeq_Pipeline.sh
# or using an array after updating path
./pipeline_array.sh
```

## Create count matrix
```bash
# Require R with dplyr
./03_count_matrix.sh
```


FastQC v0.12.1

trimmomatic v0.39

hisat2 v2.2.1

featureCounts v2.0.8



