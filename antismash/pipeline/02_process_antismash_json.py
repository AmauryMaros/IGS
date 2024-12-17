import os
import argparse
from functions import *

def main():
    parser = argparse.ArgumentParser(description="Process antismash JSON output to extract MIBiG comparison results.")
    parser.add_argument('path', type=str, help='Path to the directory containing antismash outputs')
    parser.add_argument('temp_dir', type=str, nargs='?', default=os.path.join(os.getcwd(), "temp_file"),
                        help='Path to the temporary directory for saving output files (default: ./temp_file)')

    args = parser.parse_args()

    # Check if the path is empty
    if not args.path:
        print("Error: No path provided.")
        return

    # Call the parse_json function
    region_summary_df, query_to_reference_df, similarity_score_df, blast_score_df, mibig_entries_df, cluster_blast_df = parse_json(args.path)

    # Create the temp directory in the specified or default location
    if not os.path.exists(args.temp_dir):
        os.mkdir(args.temp_dir)

    # Save DataFrames to CSV files
    region_summary_df.to_csv(os.path.join(args.temp_dir, "region_summary.csv"), index=False)
    query_to_reference_df.to_csv(os.path.join(args.temp_dir, "query_to_reference.csv"), index=False)
    similarity_score_df.to_csv(os.path.join(args.temp_dir, "similarity_score.csv"), index=False)
    blast_score_df.to_csv(os.path.join(args.temp_dir, "blast_score.csv"), index=False)
    mibig_entries_df.to_csv(os.path.join(args.temp_dir, "mibig_entries.csv"), index=False)
    cluster_blast_df.to_csv(os.path.join(args.temp_dir, "cluster_blast.csv"), index=False)

if __name__ == "__main__":
    main()

