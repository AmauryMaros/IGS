# Pipeline for processing antiSMASH results

## 1. Go to the Pipeline Directory
Navigate to the pipeline directory where the processing scripts are located.

```bash
cd path/to/pipeline
```

## 2. Get JSON Files with antiSMASH Results

This step processes the antiSMASH results by iterating through directories and extracting .json files.

## Example:
```bash
python 01_process_antismash_output.py path/to/results_antiSMASH path/to/JSON_directory
```

### Notes

* This command will iterate through all directories in ```results_antiSMASH``` and copy the ```.json``` files into ```JSON_directory```.

* ```results_antiSMASH``` contains a list of directories (one for each FASTA file processed by antiSMASH), accordingly to the ```--output-dir``` argument used in the antiSMASH command.

* ```JSON_directory``` is created if it doesn't already exist.



## 3. Extract Data from JSON Files

Once the JSON files are gathered, this step compiles data from them into several CSV files.



## Example
```bash
python 02_process_antismash_json.py path/to/JSON_directory path/to/CSV_files
```

This command generates four CSV files:

* blast score
* mibig entries
* query_to_reference
* similarity score

