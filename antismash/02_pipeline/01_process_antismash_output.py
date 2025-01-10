import os
import sys
import shutil
import subprocess

# Function to display help message
def show_help():
    print("\nUsage: script.py <antismash_results_path> <jsons_mkdir_path>")
    print("\nProcess JSON files from the specified antismash results directory.")
    print("\nArguments:")
    print("    <antismash_results_path>   Path to the directory containing antismash results.")
    print("    <jsons_mkdir_path>         Path to create the directory where JSON files will be copied.")
    print("\nOptions:")
    print("    --help                    Display this help message.\n")
    sys.exit(0)

# Function to check JSON file status by calling get_json_status.py
def process_json_file(json_file):
    try:
        # Run the external Python script on the JSON file
        result = subprocess.run(["python3", "get_json_status.py", json_file], check=True)
        return result.returncode == 0  # Return True if script succeeded
    except subprocess.CalledProcessError:
        # print(f"Error: get_json_status.py failed for {json_file}")
        return print(f"Not copied: {json_file} (no results found from antiSMASH)")

# Function to copy the valid JSON file
def copy_json_file(json_file, destination):
    try:
        shutil.copy(json_file, destination)
        print(f"Copied:     {json_file}")
    except shutil.Error as e:
        print(f"Copy failed for {json_file}: {e}")

# Main function
def main():
    # Check if the help option is passed
    if "--help" in sys.argv:
        show_help()

    # Check if the correct number of arguments is passed
    if len(sys.argv) < 3:
        print("\nError: Not enough arguments.\n")
        show_help()

    # Assign arguments to variables
    antismash_results_path = sys.argv[1]
    json_output_path = sys.argv[2]

    # Create the output directory if it doesn't exist
    os.makedirs(json_output_path, exist_ok=True)

    # List files in the antismash_results_path directory
    for entry in sorted(os.listdir(antismash_results_path)):
        # Skip hidden files or ignored files
        if entry.startswith("."):
            continue

        json_file = os.path.join(antismash_results_path, entry, f"{entry}.json")

        # Check if the JSON file exists
        if os.path.isfile(json_file):
            if process_json_file(json_file):
                # Copy the file if processing was successful
                copy_json_file(json_file, json_output_path)
            else:
                continue
                # print(f"File {json_file} is not relevant and will not be copied.")
        else:
            print(f"Warning: No JSON file found for directory {entry}")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()

