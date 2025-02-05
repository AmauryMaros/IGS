# Load required package
library(dplyr)

# List all featureCounts output files
files <- list.files("data/quants/", pattern = "_featurecounts.txt$", full.names = TRUE)

# Read first file to extract gene names
df <- read.delim(files[1], comment.char = "#")[, c(1, 7)]
colnames(df) <- c("Gene", gsub("_featurecounts.txt", "", basename(files[1])))

# Loop through the rest and merge
for (file in files[-1]) {
  temp <- read.delim(file, comment.char = "#")[, c(1, 7)]
  colnames(temp) <- c("Gene", gsub("_featurecounts.txt", "", basename(file)))
  df <- merge(df, temp, by = "Gene")
}

# Save merged count matrix
write.table(df, "data/count_matrix.txt", sep = "\t", row.names = FALSE, quote = FALSE)
