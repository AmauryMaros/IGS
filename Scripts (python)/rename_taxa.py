def rename_taxa(string):
    """
    Rename a taxa name with the first letter capitalized, followed by a "." and the rest of the name.

    Argument:
        string (str): Taxa name.

    Return:
        str: Reformatted taxa name.

    Example:
        rename_taxa("Lactobacillus_crispatus") -> "L. crispatus"
    """
  
    string_list = string.split("_")

    if len(string_list) < 2:
        return string

    return f"{string_list[0][0]}. {' '.join(string_list[1:])}"
