from functions import *
import argparse

def main():

    parser = argparse.ArgumentParser(description="Process antismash JSON output to extract MIBiG comparison results.")
    parser.add_argument('path', type=str, help='Path to the directory containing antismash outputs')

    args = parser.parse_args()

    query_to_reference_df, similarity_score_df, blast_score_df, mibig_entries_df = get_mibig_comparison(args.path)
    
    # Create a temp directory if not already existing
    temp_dir = "temp_file"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    # Save DataFrames to CSV files
    query_to_reference_df.to_csv(f"{temp_dir}/query_to_reference_df.csv", index=False)
    similarity_score_df.to_csv(f"{temp_dir}/similarity_score_df.csv", index=False)
    blast_score_df.to_csv(f"{temp_dir}/blast_score_df.csv", index=False)
    mibig_entries_df.to_csv(f"{temp_dir}/mibig_entries_df.csv", index=False)

if __name__ == "__main__":
    main()

