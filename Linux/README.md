# Usefull commands

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

## Number of file with .out extension
```bash
ls -1 *.txt | wc -l
```

## Create a symlink
```bash
ln -s <target file or directory> <link name>
```

## Number of symlinks
```bash
find . -maxdepth 1 -type l | wc -l
```


