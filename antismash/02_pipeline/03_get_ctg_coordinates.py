import pandas as pd
import os

# List to collect DataFrames
list_of_df = []

# Loop through each MAG
#for mag in genes_position['MAG'].unique():
for mag in sorted(os.listdir('/local/scratch/amaros/antismash/results_antismash/')):
    # Define the path to the clusterblast directory
    file_path = f'/local/scratch/amaros/antismash/results_antismash/{mag}/clusterblast/'

    # Check if the directory exists
    if not os.path.exists(file_path):
        print(f"Directory not found: {file_path}")
        continue

    # Loop through files in the directory
    for elt in os.listdir(file_path):
        # Construct the full file path
        full_path = os.path.join(file_path, elt)
        
        # Skip if it's not a file
        if not os.path.isfile(full_path):
            continue

        # Initialize variables
        table_lines = []
        is_table = False

        # Read the file line by line
        with open(full_path, "r") as f:
            for line in f:
                # Detect the start of the table (adjust condition as needed)
                if line.startswith("ctg"):
                    is_table = True
                # If within the table, collect lines
                if is_table:
                    # Stop if encountering an empty line or non-table line
                    if line.strip() == "" or not line[0].isalnum():
                        break
                    table_lines.append(line.strip())

        # Convert the table to a DataFrame
        if table_lines:
            try:
                table_df = pd.DataFrame(
                    [line.split() for line in table_lines],
                    columns=["Gene", "Start", "End", "Strand"]
                )
                table_df["Start"] = table_df["Start"].astype(int) + 1
                table_df["Start"] = table_df["Start"].astype(str)
                table_df['sequence'] = elt[:-7]
                list_of_df.append(table_df)
            except ValueError:
                print(f"Error processing file: {full_path}")
                continue

pd.concat(list_of_df).to_csv("/local/scratch/amaros/antismash/03_results/ctg_coordinates.csv", index=False)

