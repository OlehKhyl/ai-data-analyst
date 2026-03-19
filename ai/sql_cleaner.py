import re

def clean_sql(sql: str) -> str:
    """
    Cleans the SQL query by removing unnecessary whitespace and ensuring proper formatting.
    """
    # Remove leading and trailing whitespace
    cleaned_sql = sql.strip()
    
    if not (cleaned_sql.upper().startswith("SELECT") or cleaned_sql.upper().startswith("WITH")):
        first_select_index = cleaned_sql.upper().find("SELECT")
        first_with_index = cleaned_sql.upper().find("WITH")
        
        if first_select_index != -1:
            cleaned_sql = cleaned_sql[first_select_index:]
        elif first_with_index != -1:
            cleaned_sql = cleaned_sql[first_with_index:]

    if not cleaned_sql.upper().endswith(";"):
        first_semicolon_index = cleaned_sql.find(";")
        if first_semicolon_index != -1:
            cleaned_sql = cleaned_sql[:first_semicolon_index + 1]

    # Remove markdown headers (e.g., # Header)
    cleaned_sql = re.sub(r'#+\s*', '', cleaned_sql)
    # Remove bold/italic (e.g., **bold**, *italic*)
    cleaned_sql = re.sub(r'(\*\*|__)(.*?)\1', r'\2', cleaned_sql)
    cleaned_sql = re.sub(r'(\*|_)(.*?)\1', r'\2', cleaned_sql)
    # Remove links (e.g., [cleaned_sql](url))
    cleaned_sql = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned_sql)
    # Remove inline code (e.g., `code`)
    cleaned_sql = re.sub(r'`(.*?)`', r'\1', cleaned_sql)
    # Remove block quotes (e.g., > quote)
    cleaned_sql = re.sub(r'^>\s*', '', cleaned_sql, flags=re.MULTILINE)
    # Remove horizontal rules (e.g., --- or ***)
    cleaned_sql = re.sub(r'^[-*]{3,}\s*$', '', cleaned_sql, flags=re.MULTILINE)
    # Remove list markers (e.g., - item or * item or 1. item)
    cleaned_sql = re.sub(r'^(\*|-|\+|\d+\.)\s*', '', cleaned_sql, flags=re.MULTILINE)
    # Remove code blocks (e.g., ```code```)
    cleaned_sql = re.sub(r'```[\s\S]*?```', '', cleaned_sql, flags=re.MULTILINE)

    return cleaned_sql