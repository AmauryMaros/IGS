import os
import pandas as pd
import json
import argparse

# 1. Functions
def filter_json(data_records):
    """
    Filters antismash JSON file records. If the 'modules' key contains only 2 subkeys, 
    they are 'antismash.detection.full_hmmer' and 'antismash.detection.hmm_detection'.
    We want to filter records with more than 2 keys to get results from other detection tools.
    """
    index = []
    for i, record in enumerate(data_records):
        modules = record.get("modules", {}).keys()
        if len(modules) > 2:
            index.append(i)
    return index

def get_mibig_comparison_similarity_score(mibig_comparison, analysis_type, mag, region, ctg):
    """
    Create a DataFrame from MIBiG Comparison data extracted from the JSON output 
    corresponding to the specified analysis type (e.g., ProtoToRegion or RegionToRegion).
    """
    score = pd.DataFrame(list(mibig_comparison['by_region'][region][analysis_type]['scores_by_region'].items()), columns=['reference', 'similarity_score'])
    score['MAG'] = mag
    score['region'] = region
    score['ctg'] = ctg + 1
    score['position'] = score['reference'].apply(lambda x: x.split(": ")[1] if ": " in x else None)
    score['reference'] = score['reference'].apply(lambda x: x.split(": ")[0] if ": " in x else x)
    return score

def get_mibig_comparison_annotation(mibig_comparison, region, analysis_type):
    """
    description
    """
    annotation = mibig_comparison['by_region'][region][analysis_type]['reference_regions']
    proto_to_region_w_annotation = []
    for data in annotation.values():
        extracted_data = {col: data.get(col, None) for col in ['accession', 'products', 'organism', 'description']}
        if isinstance(extracted_data['products'], list):
            extracted_data['products'] = '; '.join(extracted_data['products'])
            df_extracted = pd.DataFrame([extracted_data]).rename(columns={"accession": "reference"})
            proto_to_region_w_annotation.append(df_extracted)

    return proto_to_region_w_annotation



def extract_mibig_comparison_data(path):
    """
    Parses all JSON files within a specified directory and extracts MIBiG Comparison data from HTLM outputs.

    Args:
        path (str): The directory path containing subfolders for each entry. Each subfolder should contain a JSON file 
                    named `<subfolder_name>.json` with the required information.

    Returns:
        tuple:
            proto_to_region (pandas.DataFrame): A DataFrame containing extracted ProtoToRegion MIBiG comparison data for all records.
            region_to_region (pandas.DataFrame): A DataFrame containing extracted RegionToRegion MIBiG comparison data for all records.
    """
    ignore_patterns = {".DS_Store", ".cache"}

    list_protocluster_to_region_w_similarity = []
    list_region_to_region_w_similarity = []

    # Iterate over all directories in the specified path
    for elt in sorted(os.listdir(path)):
        if elt not in ignore_patterns and os.path.isdir(os.path.join(path, elt)):
            print(f"Processing file: {elt}")

            try:
                with open(f"{path}/{elt}/{elt}.json", 'r') as f:
                    json_file = json.load(f)
            except Exception as e:
                print(f"Error reading {elt}.json: {e}")
                continue
            
            # Get indices for records with desired key conditions
            indices = filter_json(json_file.get("records", []))

            # Initialize DataFrames
            proto_to_region = pd.DataFrame()
            region_to_region = pd.DataFrame()

            # Iterate over each index in the filtered records
            for ctg in indices:

                proto_to_region_w_annotation = []
                region_to_region_w_annotation = []
                mibig_comparison = json_file['records'][ctg]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']

                # Iterate over each region found in the sequence
                for region in mibig_comparison['by_region'].keys():

                    # Get reference and similarity score for both ProtoToRegion and RegionToRegion analysis
                    proto_to_region_by_key = get_mibig_comparison_similarity_score(mibig_comparison, "ProtoToRegion_RiQ", elt, region, ctg)
                    region_to_region_by_key = get_mibig_comparison_similarity_score(mibig_comparison, "RegionToRegion_RiQ", elt, region, ctg)

                    # Get ProtoToRegion and RegionToRegion annotations
                    proto_to_region_w_annotation = get_mibig_comparison_annotation(mibig_comparison, region, "ProtoToRegion_RiQ")
                    region_to_region_w_annotation = get_mibig_comparison_annotation(mibig_comparison, region, "RegionToRegion_RiQ")

                    # Merge similarity scores with annotations
                    if proto_to_region_w_annotation:
                        proto_to_region_by_key = pd.merge(proto_to_region_by_key, pd.concat(proto_to_region_w_annotation), on="reference", how="left")
                    if region_to_region_w_annotation:
                        region_to_region_by_key = pd.merge(region_to_region_by_key, pd.concat(region_to_region_w_annotation), on="reference", how="left")

                    # Concatenate data if not empty
                    if not proto_to_region_by_key.empty:
                        proto_to_region = pd.concat([proto_to_region, proto_to_region_by_key], axis=0)
                    if not region_to_region_by_key.empty:
                        region_to_region = pd.concat([region_to_region, region_to_region_by_key], axis=0)

            # Append DataFrames to lists for later concatenation
            if not proto_to_region.empty:
                list_protocluster_to_region_w_similarity.append(proto_to_region)
            if not region_to_region.empty:
                list_region_to_region_w_similarity.append(region_to_region)

    # Concatenate final DataFrames
    df_proto_final = pd.concat(list_protocluster_to_region_w_similarity, ignore_index=True) if list_protocluster_to_region_w_similarity else pd.DataFrame()
    df_region_final = pd.concat(list_region_to_region_w_similarity, ignore_index=True) if list_region_to_region_w_similarity else pd.DataFrame()

    return df_proto_final, df_region_final


def main():
    parser = argparse.ArgumentParser(description="Process antismash JSON output to extract MIBiG comparison results.")
    parser.add_argument('path', type=str, help='Path to the directory containing antismash outputs')

    args = parser.parse_args()

    proto_to_region, region_to_region = extract_mibig_comparison_data(args.path)
    
    # Create a temp directory if not already existing
    temp_dir = "temp_file"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    # Save DataFrames to CSV files
    proto_to_region.to_csv(f"{temp_dir}/protocluster_to_region.csv", index=False)
    region_to_region.to_csv(f"{temp_dir}/region_to_region.csv", index=False)


if __name__ == "__main__":
    main()
