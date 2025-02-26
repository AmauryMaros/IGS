#!/bin/bash

# Set the name of the LaTeX file
LATEX_FILE="main.tex"

# Compile the LaTeX file with pdflatex
pdflatex $LATEX_FILE

# Run pdflatex twice to ensure proper references and table of contents
pdflatex $LATEX_FILE

# Clean up temporary files generated by LaTeX
rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk

echo "Compilation complete and temporary files removed."

# Export to .docx
# pandoc main.tex -o main.docx
