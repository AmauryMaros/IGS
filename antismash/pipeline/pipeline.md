# **Pipeline Explanation**

## **Scripts Overview**

### 01_process_antismash_output.py
- **Function**:  
  Iterates through all antiSMASH output directories and copies JSON files of interest to a desired path.  
- **Output**:  
  jsons directory  
- **Contents**:  
  A directory containing JSON files with significant results from antiSMASH analysis.  

---

### 02_process_antismash_json.py
- **Function**:  
  Iterates through all JSON files and parses relevant data.  
- **Outputs**:  

| **File Name**             | **Description**                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| region_summary.csv      | Compilation of all “Overview” results from the HTML output.                  |
| query_to_reference.csv  | Compilation of all results corresponding to the “MIBiG comparison” tab in HTML output. |
| similarity_score.csv    | *To be determined*.                                                          |
| blast_score.csv         | Compilation of all BLAST analyses performed by antiSMASH.                    |
| mibig_entries.csv     | Compilation of all MIBiG hits as presented in the HTML pages within the region directory in the *knownclusterblast* folder. |
| cluster_blast.csv      | Compilation of all results obtained using the ClusterBlast algorithm in antiSMASH. |

- **Contents**:  
  A directory containing parsed JSON files with significant results from antiSMASH.  


### 03_get_ctg_coordinates.py

- **Function**:  
  Extract all coordinates of genes detected by antismash
- **Output**:  
  Ctg_coordinates.csv 
- **Contents**:  
  Csv file with unique identifier for each gene, the coordinates within the sequence in nucleotide and the strand.


### 04_get_ctg_sequences.py

- **Function**:  
  Extract all sequences of genes from 03_get_ctg_coordinates.py
- **Output**:  
  antismash_gene_sequences.fasta
- **Contents**:  
  FASTA with unique header for each gene and their corresponding sequences.

### 05_blast_ctg.py

- **Function**:  
  BLAST VIRGO2 sequences against a BLAST database build from  Antismash_gene_sequences.fasta
- **Output**:  
  to write
- **Contents**:  
  to write
