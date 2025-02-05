!/bin/bash

#SBATCH --job-name=RNAseq
#SBATCH --output=logs/RNAseq_%A_%a.out
#SBATCH --error=logs/RNAseq_%A_%a.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --array=1-12

# Activate conda env with required packages
source /usr/local/packages/miniconda3/etc/profile.d/conda.sh
conda activate /local/scratch/amaros/.conda/envs/RNAseq_env/

# Get the sample name based on the array task ID
sample=$(sed -n "${SLURM_ARRAY_TASK_ID}p" file_list.txt)

# Print task information
echo "Running task for sample: $sample (Task ID: ${SLURM_ARRAY_TASK_ID})"

# Directories
raw_R1="data/raw/${sample}_1.fq.gz"
raw_R2="data/raw/${sample}_2.fq.gz"
trimmed_R1="data/trimm/${sample}_1_trimmed.fastq"
trimmed_R2="data/trimm/${sample}_2_trimmed.fastq"
unpaired_R1="data/trimm/${sample}_1_unpaired.fastq"
unpaired_R2="data/trimm/${sample}_2_unpaired.fastq"
bam_output="data/bam/${sample}.bam"
featurecounts_output="data/quants/${sample}_featurecounts.txt"

# Step 1: Run FASTQC on raw data
echo "Running FastQC on raw data for $sample"
fastqc "$raw_R1" -o FASTQC_report/raw
fastqc "$raw_R2" -o FASTQC_report/raw

# Step 2: Run TRIMMOMATIC for paired-end reads
echo "Running Trimmomatic on $sample"
trimmomatic PE -threads 4 "$raw_R1" "$raw_R2" \
    "$trimmed_R1" "$unpaired_R1" \
    "$trimmed_R2" "$unpaired_R2" \
    TRAILING:10 -phred33

# Step 3: Run FASTQC on trimmed files
echo "Running FastQC on trimmed data for $sample"
fastqc "$trimmed_R1" -o FASTQC_report/trimm
fastqc "$trimmed_R2" -o FASTQC_report/trimm

# Step 4: Run HISAT2 for genome alignment (Paired-End)
echo "Running HISAT2 on $sample"
/usr/local/packages/hisat2/hisat2 -p 8 --rna-strandness RF -x Genome/grch38/genome -1 "$trimmed_R1" -2 "$trimmed_R2" | samtools sort -o "$bam_output"

# Step 5: Run featureCounts - Quantification
echo "Running featureCounts on $sample"
featureCounts -T 4 -p -S 2 -a Genome/Homo_sapiens.GRCh38.113.gtf -o "$featurecounts_output" "$bam_output"

# Deactivate environment when job is done
conda deactivate

# Print total runtime
echo "Finished processing $sample"
