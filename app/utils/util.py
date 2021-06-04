def escape_like(string, escape_char="\\"):
    """escape the string paremeter used in SQL like expressions"""
    return (
        string.replace(escape_char, escape_char * 2)
        .replace("%", escape_char + "%")
        .replace("_", escape_char + "_")
    )
