import os
import pandas as pd
import json
import argparse

# 1. Function to filter the JSON file resulting from antismash

def filter_json(data_records):
    """
    Filters antismash JSON file records. If the module key contains only 2 keys, 
    they are 'antismash.detection.full_hmmer' and 'antismash.detection.hmm_detection'.
    We want to filter records with more than 2 keys to have get others detection tools results.
    """
    index = []
    for i in range(len(data_records)):
        modules = data_records[i]["modules"].keys()
        if len(modules) > 2:
            index.append(i)
    return index

# 2. Function to parse JSON files

def parse_json(path):

    """
    Parses all JSON files within a specified directory and extracts BLAST and MIBiG information.

    Args:
        path (str): The directory path containing subfolders for each entry. Each subfolder should contain a JSON file 
                    named `<subfolder_name>.json` with the required information.

    Returns:
        tuple:
            df_blast_final (pandas.DataFrame): A DataFrame containing extracted BLAST data for all records.
            df_mibig_final (pandas.DataFrame): A DataFrame containing extracted MIBiG data for all records.
    """
        
    list_blast = []
    list_mibig = []

    ignore_patterns = {".DS_Store", ".cache"}

    for elt in os.listdir(path):
        if elt not in ignore_patterns:
            print(f"Processing file: {elt}")

            try:
                with open(f"{path}/{elt}/{elt}.json", 'r') as f:
                    json_file = json.load(f)
            except Exception as e:
                print(f"Error reading {elt}.json: {e}")
                continue

            index_ = filter_json(json_file["records"])

            rows_blast = []
            df_mibig_list = []

            for i in index_:
                
                # Get the Bin_ID and Contig_ID
                bin_id = json_file["input_file"]
                contig_id = json_file["records"][i]["modules"]["antismash.modules.clusterblast"]["record_id"]

                # Get the blast_info and mibig_entries
                blast_info = json_file["records"][i]["modules"]["antismash.modules.clusterblast"]["general"]["results"][0]["ranking"][1][1]["pairings"]
                modules = json_file["records"][i]["modules"]["antismash.modules.clusterblast"]["knowncluster"]

                # Check if 'mibig_entries' exists in the modules
                if "mibig_entries" in modules:
                    mibig_entries = modules['mibig_entries']['1']  # 'mibig_entries' is a dictionary with ctg_# as keys
                    # Add mibig_entries for the current tag_id
                    for ctg_name in mibig_entries.keys():
                        df_tag_id = pd.DataFrame(mibig_entries[ctg_name])
                        df_tag_id['ctg_tag_id'] = ctg_name
                        df_mibig_list.append(df_tag_id)
                else:
                    print(f"No 'mibig_entries' found for record {i}")

                # Add BLAST information to rows_blast
                for blast in blast_info:
                    ctg_name = blast[0].split("|")[4]
                    blast_data = {
                        "bin_id": bin_id,
                        "contig_id": contig_id,
                        "ctg": ctg_name.split("_")[0],
                        "ctg_tag_id": ctg_name,
                        "ctg_cordinates": blast[0].split("|")[2],
                        "blast_name": blast[2]["name"], 
                        "blast_genecluster": blast[2]["genecluster"],
                        "blast_annotation": blast[2]["annotation"],
                        "blast_perc_coverage": blast[2]["perc_coverage"],
                        "blast_perc_ident": blast[2]["perc_ident"],
                        "blast_blastscore": blast[2]["blastscore"],
                        "blast_evalue": blast[2]["evalue"],
                        "blast_locus_tag": blast[2]["locus_tag"],
                    }

                    rows_blast.append(blast_data)

            # Convert rows to a DataFrame
            df_blast = pd.DataFrame(rows_blast)

            # Concatenate all DataFrames for mibig entries
            if df_mibig_list:
                df_mibig = pd.concat(df_mibig_list, axis=0, ignore_index=True)
                df_mibig = df_mibig.rename(columns={
                    0: "mibig_protein",
                    1: "description",
                    2: "mibig_cluster",
                    3: "region",
                    4: "mibig_product",
                    5: "percentage_id",
                    6: "blast_score",
                    7: "percentage_coverage",
                    8: "evalue"
                })
            else:
                df_mibig = pd.DataFrame()  # Create an empty DataFrame if no mibig entries were found

            list_blast.append(df_blast)
            list_mibig.append(df_mibig)

    if list_blast:
        df_blast_final = pd.concat(list_blast, ignore_index=True)
    else:
        df_blast_final = pd.DataFrame()  # Create an empty DataFrame if no data

    if list_mibig:
        df_mibig_final = pd.concat(list_mibig, ignore_index=True)
    else:
        df_mibig_final = pd.DataFrame()  # Create an empty DataFrame if no data

    return df_blast_final, df_mibig_final

def main():
    parser = argparse.ArgumentParser(description="Process antismash JSON output to extract blast and mibig results.")
    parser.add_argument('path', type=str, help='Path to the directory containing antismash outputs')
    parser.add_argument('blast_output', type=str, help='Filename for the blast output CSV')
    parser.add_argument('mibig_output', type=str, help='Filename for the mibig output CSV')

    args = parser.parse_args()

    df_blast, df_mibig = parse_json(args.path)

    # Save DataFrames to CSV files
    df_blast.to_csv(args.blast_output, index=False)
    df_mibig.to_csv(args.mibig_output, index=False)

if __name__ == "__main__":
    main()
