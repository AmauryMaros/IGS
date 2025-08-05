# Usefull commands

## awk
```bash
Print seq #19 in fasta file
awk 'BEGIN {seq=18} /^>/ {header=$0; next} seq-- == 0 {print header "\n" $0; exit}' MAG00001.fasta
```

## Extract lines from file
```bash
# Ex: lines 10 to 35
sed -n '10,35p' input.txt > output.txt
```

## Inline loop
```bash
for i in {1..12}; do cat "rsem_${i}.err" | tail -n 5;done
for i in *.err; do cat "$i"; done
```

## Number of lines in a file
```bash
wc -l <file>
```

## Number of columns in a file
```bash
awk '{print NF; exit}' path/to/file.txt
```

## Number of elements in a directory
``` bash
ls -1A | wc -l
```

## Number of sequences in FASTA/FASTQ
Using grep
```bash
grep -c "^>" file.fasta
```

Using sektq
```bash
seqtk comp file.fasta | wc -l
```

## Number of file with .txt extension
```bash
ls -1 *.txt | wc -l
```

## Number of non empty file in a directory
```bash
find . -type f -size +0c
```


## Create a symlink
```bash
ln -s <target file or directory> <link name>
```

## Number of symlinks
```bash
find . -maxdepth 1 -type l | wc -l
```


