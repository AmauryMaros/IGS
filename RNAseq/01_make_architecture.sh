#!/bin/bash

# Create output directories if they don't exist
mkdir -p data/trimm
mkdir -p data/bam
mkdir -p data/quants
mkdir -p FASTQC_report/raw
mkdir -p FASTQC_report/trimm
mkdir -p Genome

# Download and extract reference genome
wget -P Genome https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
tar -xvzf Genome/grch38_genome.tar.gz -C Genome/

# Download and extract gene annotations (GTF)
wget -P Genome https://ftp.ensembl.org/pub/release-113/gtf/homo_sapiens/Homo_sapiens.GRCh38.113.gtf.gz
gunzip Genome/Homo_sapiens.GRCh38.113.gtf.gz

# Make list of samples for array
ls data/raw/*_1.fq.gz | sed 's#.*raw/##' | sed 's/_1.fq.gz//' | sort -V > file_list.txt
