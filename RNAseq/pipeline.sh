#!/bin/bash

# Activate conda env with required packages if needed
source ~/miniconda3/bin/activate RNAseq

# Initiate a timer
SECONDS=0

### 0. Create directory architecture and download necessary data

# Create output directories if they don't exist
mkdir -p data/trimm
mkdir -p data/bam
mkdir -p data/quants
mkdir -p FASTQC_report/raw
mkdir -p FASTQC_report/trimm
mkdir -p Genome

# Symlink raw data to data/raw
for file in "path_to_raw_data/"*.fq.gz; do 
    ln -sf "$file" "data/raw/$(basename "$file")";
done

# Create file list for array
ls data/raw/*_1.fq.gz | sed 's#.*raw/##' | sed 's/_1.fq.gz//' | sort -V > file_list.txt

# Download and extract reference genome
wget -P Genome https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
tar -xvzf Genome/grch38_genome.tar.gz -C Genome/

# Download and extract gene annotations (GTF)
wget -P Genome https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Homo_sapiens.GRCh38.113.gtf.gz
gunzip Genome/Homo_sapiens.GRCh38.113.gtf.gz

### 1. Run FASTQC on RAW data

for file in data/raw/*.fq.gz; do
    echo "Running FastQC on $file"
    fastqc "$file" -o FASTQC_report/raw
done

### 2. Run TRIMMOMATIC for paired-end reads

for sample in $(cat file_list.txt); do
    echo "Running Trimmomatic on $sample"

    # Define input/output file names
    raw_R1="data/raw/${sample}_1.fq.gz"
    raw_R2="data/raw/${sample}_2.fq.gz"
    trimmed_R1="data/trimm/${sample}_1_trimmed.fastq"
    trimmed_R2="data/trimm/${sample}_2_trimmed.fastq"
    unpaired_R1="data/trimm/${sample}_1_unpaired.fastq"
    unpaired_R2="data/trimm/${sample}_2_unpaired.fastq"

    # Run Trimmomatic PE (Paired-End)
    trimmomatic PE -threads 4 "$raw_R1" "$raw_R2" \
        "$trimmed_R1" "$unpaired_R1" \
        "$trimmed_R2" "$unpaired_R2" \
        TRAILING:10 -phred33

    # Run FASTQC on trimmed files
    fastqc "$trimmed_R1" -o FASTQC_report/trimm
    fastqc "$trimmed_R2" -o FASTQC_report/trimm
done

### 3. Run HISAT2 for genome alignment (Paired-End)

for sample in $(cat file_list.txt); do
    echo "Running HISAT2 on $sample"

    trimmed_R1="data/trimm/${sample}_1_trimmed.fastq"
    trimmed_R2="data/trimm/${sample}_2_trimmed.fastq"
    bam_output="data/bam/${sample}.bam"

    # Run HISAT2 alignment
    hisat2 -p 8 --rna-strandness RF -x Genome/grch38/genome \
        -1 "$trimmed_R1" -2 "$trimmed_R2" | samtools sort -o "$bam_output"

    echo "Finished processing $sample"
done

### 4. Run featureCounts - Quantification

for sample in $(cat file_list.txt); do
    bam_file="data/bam/${sample}.bam"
    output_file="data/quants/${sample}_featurecounts.txt"

    echo "Running featureCounts on $bam_file..."
    featureCounts -T 4 -p -S 2 -a Genome/Homo_sapiens.GRCh38.113.gtf -o "$output_file" "$bam_file"
done

# Deactivate environment when job is done
conda deactivate

# Print total runtime
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
