import os
import pandas as pd
import json

def get_index(json_file: dict) -> list:
    """
    Filters antiSMASH JSON file records. If the 'modules' key contains only 2 subkeys, 
    they are 'antismash.detection.full_hmmer' and 'antismash.detection.hmm_detection'.
    We want to filter records with more than 2 keys to get results from other detection tools.

    Parameters
    ----------
    json_file : dict

    Returns
    -------
    index : list of integers
    """

    index = []
    data_records = json_file.get("records", [])
    for i, record in enumerate(data_records):
        modules = record.get("modules", {}).keys()
        if len(modules) > 2:
            index.append(i)

    return index

def get_blast_scores(json_file, idx):
    """
    Get BLAST scores from antiSMASH.

    Parameters
    ----------
    json_file : dict
        JSON file from antiSMASH output.
    idx : int
        Index of the record in the JSON file.

    Returns
    -------
    df_blast : DataFrame
        DataFrame of results.
    """
    list_blast = []

    blast = json_file["records"][idx]["modules"]["antismash.modules.clusterblast"]["general"]["results"]
    for region in range(len(blast)):
        ranking = blast[region]['ranking']
        for hit in range(len(ranking)):
            blast_info = ranking[hit][1]['pairings']
            for score in blast_info :
                ctg_name = score[0].split("|")[4]
                coordinate = score[0].split("|")[2]
                blast_data = score[2]
                blast_data['coordinate'] = coordinate
                blast_data['sequence'] = json_file["records"][idx]['id']
                blast_data['region'] = f"{idx+1}.{region+1}"
                blast_data['ctg'] = ctg_name
                list_blast.append(blast_data)
    df = pd.DataFrame(list_blast)
    return df

def get_mibig_entries(json_file: dict, idx: int) -> pd.DataFrame:
    """
    Extract MIBiG entries from antiSMASH output.

    Parameters
    ----------
    json_file : dict
        JSON file from antiSMASH output.
    idx : int
        Index of the record in the JSON file.

    Returns
    -------
    pd.DataFrame
        DataFrame of MIBiG entries.
    """
    
    try:
        # Access modules for the given index
        modules = json_file["records"][idx]["modules"]["antismash.modules.clusterblast"]["knowncluster"]
    except (KeyError, IndexError) as e:
        print(f"Error accessing modules or record: {e}")
        return pd.DataFrame()

    df_mibig_list = []

    # Check if 'mibig_entries' exists in the modules
    if "mibig_entries" in modules:
        for region in modules['mibig_entries'].keys():
            mibig_entries = modules['mibig_entries'][region]  # 'mibig_entries' is a dictionary with ctg_# as keys
            # Add mibig_entries for the current tag_id
            for ctg_name in mibig_entries.keys():
                df_tag_id = pd.DataFrame(mibig_entries[ctg_name])
                df_tag_id = df_tag_id.drop(columns=[3],axis=1)
                df_tag_id['sequence'] = json_file["records"][idx]['id']
                df_tag_id['region'] = f"{idx+1}.{int(region)}"
                df_tag_id['ctg'] = ctg_name
                df_mibig_list.append(df_tag_id)
    else:
        print(f"No 'mibig_entries' found for record {idx}")
        
    # Concatenate all DataFrames for mibig entries
    if df_mibig_list:
            df_mibig = pd.concat(df_mibig_list, axis=0, ignore_index=True)
            df_mibig = df_mibig.rename(columns={
                    0: "mibig_protein",
                    1: "description",
                    2: "mibig_cluster",
                    # 3: "region",
                    4: "mibig_product",
                    5: "percentage_id",
                    6: "blast_score",
                    7: "percentage_coverage",
                    8: "evalue"
                })
            # df_mibig['sequence'] = json_file["records"][idx]['id']
    else:
            df_mibig = pd.DataFrame()

    return df_mibig

def get_query_to_reference_match(json_file: dict, idx: int) -> pd.DataFrame:
    """
    Extract data from MIBiG Comparison tab in antiSMASH HTML output.
    
    This function take as input a JSON file for a FASTA file and return a dataframe.
    The dataframe contains information about the matching between the query and the references, showm in the html page
    by a visualization of both the query and 

    Parameters
    ----------
    json_file : dict
        json file from antismash output.
    idx : int
        Index of the record in the JSON file.

    Returns
    -------
    df : DataFrame
        DataFrame of results.
    """

    ctg = []

    try:
        results = json_file['records'][idx]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']['by_region']
    except KeyError as e:
        print(f"KeyError: {e}")
        return pd.DataFrame()
    
    for region in results.keys():
        for bgc in results[region]['ProtoToRegion_RiQ']['hits'].keys():
            ctg_table = results[region]['ProtoToRegion_RiQ']['hits'][bgc]
            ctg_table_df = pd.DataFrame(ctg_table).transpose()
            ctg_table_df['sequence'] = json_file['records'][idx]['id']
            ctg.append(ctg_table_df)

    df = pd.concat(ctg, axis=0).reset_index().rename(columns={"index":"protein"}) if ctg else pd.DataFrame()
    return df


def get_similarity_score_w_annotation(json_file: dict, idx: int) -> pd.DataFrame:
    """
    Extract data from MIBiG Comparison tab in antiSMASH HTML output.
    
    This function return the similarity score for different kinds of analysis (ex: Protocluster to Region) with annotation related to each reference

    Parameters
    ----------
    json_file : dict
        json file from antismash output.
    idx : int
        Index of the record in the JSON file.

    Returns
    -------
    df : DataFrame
        DataFrame of results.
    """

    try:
        results = json_file['records'][idx]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']['by_region']
    
    except KeyError as e:
        print(f"KeyError: {e}")
        return pd.DataFrame()
    

    data_score = {}
    data_annotation = []

    for region_idx in results.keys():
        for analysis in results[region_idx].keys():
            scores_by_region = results[region_idx][analysis]['scores_by_region']
            if scores_by_region != {}:
                data_score[analysis] = scores_by_region
                similarity_score = pd.DataFrame(data_score).reset_index().rename(columns={"index":"Reference"})
                similarity_score['Position'] = similarity_score['Reference'].apply(lambda x : x.split(": ")[1])
                similarity_score['Reference'] = similarity_score['Reference'].apply(lambda x : x.split(": ")[0])
                similarity_score['Region'] = f"{idx+1}.{region_idx}"
                similarity_score['Sequence'] = json_file['records'][idx]['id']
            else :
                similarity_score = None
            
            reference_regions = results[region_idx][analysis]['reference_regions']
            if reference_regions != {}:
                for bgc in reference_regions.keys():
                        hit = reference_regions[bgc]
                        entry = {
                        'Reference': hit.get('accession'),
                        'Type': '; '.join(hit.get('products')),
                        'Compound': hit.get('description'),
                        'Organism': hit.get('organism')
                        }
                        data_annotation.append(entry)
            else :
                data_annotation = None
        if (similarity_score is not None) and (data_annotation is not None):    # the or & and statements in Python require TRUTH values 
            df = pd.merge(similarity_score, pd.DataFrame(data_annotation), on="Reference", how="left")
            df = df.drop_duplicates()
        else :
            df = None

    return df


def parse_json(path):
    """
    Extract data from MIBiG Comparison tab in antiSMASH HTML output.
    
    This function iterate over all directories outputs generated by antiSMASH on multiples FASTA files. 

    Parameters
    ----------
    path : str
        path to the directory containing all antiSMASH directories outputs

    Returns
    -------
    query_to_reference_df : DataFrame
        DataFrame of results.
    similarity_score_df : DataFrame
        DataFrame of results.
    blast_score_df : DataFrame
        DataFrame of results.
    mibig_entries_df : DataFrame
        DataFrame of results.  
    """

    # Initialize empty lists
    query_to_reference = []
    similarity_score = []
    blast_score = []
    mibig_entries = []

    # Iterate over all directories in the specified path
    ignore_patterns = {".DS_Store", ".cache"}

    # print(os.listdir(path))
    for elt in sorted(os.listdir(path)):

        if elt not in ignore_patterns :
            print(f"Processing file: {elt}")
            try:
                with open(os.path.join(path, elt), 'r') as f:   #,f"{elt}.json"
                    json_file = json.load(f)
            except Exception as e:
                print(f"Error reading {elt}: {e}. Skipping file.")
                continue
            
            # Get indices for records with desired key conditions
            indices = get_index(json_file)

            # Iterate over all sequences with results
            for idx in indices :
                query_to_reference.append(get_query_to_reference_match(json_file, idx))
                similarity_score.append(get_similarity_score_w_annotation(json_file, idx))
                blast_score.append(get_blast_scores(json_file, idx))
                mibig_entries.append(get_mibig_entries(json_file, idx))

    query_to_reference_df = pd.concat(query_to_reference, ignore_index=True) if query_to_reference else pd.DataFrame()
    similarity_score_df = pd.concat(similarity_score, ignore_index=True) if similarity_score else pd.DataFrame()
    blast_score_df = pd.concat(blast_score, ignore_index=True) if blast_score else pd.DataFrame()
    mibig_entries_df = pd.concat(mibig_entries, ignore_index=True) if mibig_entries else pd.DataFrame()

    return query_to_reference_df, similarity_score_df, blast_score_df, mibig_entries_df
