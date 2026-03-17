def clean_sql(sql: str) -> str:
    """
    Cleans the SQL query by removing unnecessary whitespace and ensuring proper formatting.
    """
    # Remove leading and trailing whitespace
    cleaned_sql = sql.strip()
    
    # Replace multiple spaces with a single space
    cleaned_sql = ' '.join(cleaned_sql.split())
    
    if not cleaned_sql.upper().startswith("SELECT"):
        first_select_index = cleaned_sql.upper().find("SELECT")
        if first_select_index != -1:
            cleaned_sql = cleaned_sql[first_select_index:]
        else:            
            raise ValueError("The SQL query must contain a SELECT statement.")

    if not cleaned_sql.upper().endswith(";"):
        first_semicolon_index = cleaned_sql.find(";")
        if first_semicolon_index != -1:
            cleaned_sql = cleaned_sql[:first_semicolon_index + 1]
        else:
            raise ValueError("The SQL query must end with a semicolon.")

    return cleaned_sql