# RNA Seq pipeline

## Create conda envs with required packages
```bash
conda create -n RNAseq_env python=3.8
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

FastQC v0.12.1
trimmomatic v0.39
hisat2 v2.2.1
featureCounts v2.0.8

Python 3.8.16
