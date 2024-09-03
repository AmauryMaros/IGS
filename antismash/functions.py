import os
import pandas as pd
import json

# 1. Functions

def filter_json(json_file):
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
        json file from antismash output.
    idx : list of integers
        sequence from FASTA file.

    Returns
    -------
    df_blast : DataFrame
        DataFrame of results.
    """

    rows_blast = []
    blast = json_file["records"][idx]["modules"]["antismash.modules.clusterblast"]["general"]["results"]

    for region in range(len(blast)):
        ranking = blast[region]['ranking']
        for hit in range(len(ranking)):
            blast_info = ranking[hit][1]['pairings']
            for blast in blast_info:
                ctg_name = blast[0].split("|")[4]
                blast_data = {
                            "bin_id": json_file["input_file"],
                            "contig_id": json_file["records"][idx]["modules"]["antismash.modules.clusterblast"]["record_id"],
                            "ctg": ctg_name.split("_")[0],
                            "ctg_tag_id": ctg_name,
                            "ctg_cordinates": blast[0].split("|")[2],
                            "blast_name": blast[2]["name"], 
                            "blast_genecluster": blast[2]["genecluster"],
                            "blast_annotation": blast[2]["annotation"],
                            "blast_perc_coverage": blast[2]["perc_coverage"],
                            "blast_perc_ident": blast[2]["perc_ident"],
                            "blast_score": blast[2]["blastscore"],
                            "blast_evalue": blast[2]["evalue"],
                            "blast_locus_tag": blast[2]["locus_tag"],
                        }
                rows_blast.append(blast_data)
    # Convert rows to a DataFrame
    df_blast = pd.DataFrame(rows_blast)

    return df_blast



def get_mibig_entries(json_file, idx):
    """
    Extract MIBiG entries from antiSMASH.

    Parameters
    ----------
    json_file : dict
        json file from antismash output.
    idx : list of integers
        sequence from FASTA file.

    Returns
    -------
    df_mibig : DataFrame
        DataFrame of results.
    """

    modules = json_file["records"][idx]["modules"]["antismash.modules.clusterblast"]["knowncluster"]
    df_mibig_list = []

    # Check if 'mibig_entries' exists in the modules
    if "mibig_entries" in modules:
        for region in modules['mibig_entries'].keys():
            mibig_entries = modules['mibig_entries'][region]  # 'mibig_entries' is a dictionary with ctg_# as keys
            # Add mibig_entries for the current tag_id
            for ctg_name in mibig_entries.keys():
                df_tag_id = pd.DataFrame(mibig_entries[ctg_name])
                df_tag_id['ctg_tag_id'] = ctg_name
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
                    3: "region",
                    4: "mibig_product",
                    5: "percentage_id",
                    6: "blast_score",
                    7: "percentage_coverage",
                    8: "evalue"
                })
    else:
            df_mibig = pd.DataFrame()

    return df_mibig

def get_query_to_reference_match(json_file, idx):
    """
    Extract data from MIBiG Comparison tab in antiSMASH HTML output.
    
    This function take as input a JSON file for a FASTA file and return a dataframe.
    The dataframe contains information about the matching between the query and the references, showm in the html page
    by a visualization of both the query and 

    Parameters
    ----------
    json_file : dict
        json file from antismash output.
    idx : list of integers
        sequence from FASTA file.

    Returns
    -------
    df : DataFrame
        DataFrame of results.
    """

    ctg = []
    results = json_file['records'][idx]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']['by_region']
    for region in results.keys():
        for bgc in results[region]['ProtoToRegion_RiQ']['hits'].keys():
            ctg_table = results[region]['ProtoToRegion_RiQ']['hits'][bgc]
            ctg.append(pd.DataFrame(ctg_table).transpose())

    df = pd.concat(ctg, axis=0).reset_index().rename(columns={"index":"protein"}) if ctg else pd.DataFrame()
    return df


def get_similarity_score_w_annotation(json_file, idx):
    """
    Extract data from MIBiG Comparison tab in antiSMASH HTML output.
    
    This function return the similarity score for different kinds of analysis (ex: Protocluster to Region) with annotation related to each reference

    Parameters
    ----------
    json_file : dict
        json file from antismash output.
    idx : list of integers
        sequence from FASTA file.

    Returns
    -------
    df : DataFrame
        DataFrame of results.
    """

    results = json_file['records'][idx]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']['by_region']
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
                similarity_score['Region'] = idx
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

def get_mibig_comparison_score(json_file, idx):

    results = json_file['records'][idx]['modules']['antismash.modules.cluster_compare']['db_results']['MIBiG']['by_region']
    data_score = []
    for region_idx in results.keys():
        for analysis in results[region_idx].keys():
            details = results[region_idx][analysis]['details']['details']
            
            # Check if 'details' is a list or a dictionary
            if isinstance(details, dict):
                for bgc in details.keys():
                    score = details[bgc]
                    
                    # Check if 'refs' is a list or a dictionary
                    if isinstance(score, dict):
                        for bgc in score.keys():
                            df = pd.DataFrame(score[bgc])
                            df['bgc'] = bgc
                            data_score.append(df)
                    elif isinstance(score, list):
                        # Handle the case where 'refs' is a list
                        data_score.extend(score)
            elif isinstance(details, list):
                # Handle the case where 'details' is a list
                data_score.extend(details)

    # Check the results in data_score
    pd.DataFrame(data_score)


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
    for elt in sorted(os.listdir(path)):
        if elt not in ignore_patterns and os.path.isdir(os.path.join(path, elt)):
            print(f"Processing file: {elt}")
            try:
                with open(os.path.join(path, elt, f"{elt}.json"), 'r') as f:
                    json_file = json.load(f)
            except Exception as e:
                print(f"Error reading {elt}.json: {e}. Skipping file.")
                continue
            
            # Get indices for records with desired key conditions
            indices = filter_json(json_file)

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

