import json
import sys

def get_index(json_file: dict) -> list:
    index = []
    data_records = json_file.get("records", [])
    for i, record in enumerate(data_records):
        modules = record.get("modules", {}).keys()
        if len(modules) > 2:
            index.append(i)
    return index

def main(json_file_path: str):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    index = get_index(data)
    
    if index:
        sys.exit(0)  # Relevant
    else:
        # print(f"Not copied: {json_file_path} (no results found from antiSMASH)")
        sys.exit(1)  # Not relevant

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_json_status.py <json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    main(json_file_path)
