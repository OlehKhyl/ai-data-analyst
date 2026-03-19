import re
from ai.schema_context import get_all_tables_names, get_all_columns_names

TABLE_NAMES = get_all_tables_names()
COLUMN_NAMES = get_all_columns_names()

PROHIBITED_KEYWORDS = {
    "DROP",
    "DELETE",
    "ALTER",
    "TRUNCATE",
    "INSERT",
    "UPDATE",
    "CREATE",
    "RENAME"
}

AGGREGATE_FUNCTIONS = {
    "COUNT(",
    "SUM(",
    "AVG(",
    "MIN(",
    "MAX("
}

def validate_sql_query(query: str) -> str:
    upper_query = query.upper().strip()

    if any(re.search(r'\b' + keyword + r'\b', upper_query) for keyword in PROHIBITED_KEYWORDS):
        raise ValueError("The generated SQL query contains prohibited keywords.")

    if not upper_query.startswith("SELECT") and not upper_query.startswith("WITH"):
        raise ValueError("The generated SQL query must contain a SELECT or WITH statement.")

    if re.search(r'\bSELECT\s+\*', upper_query):
        raise ValueError("The generated SQL query should not use SELECT *; please specify the columns explicitly.")

    if upper_query.count(";") > 1:
        raise ValueError("The generated SQL query shouldn't contain multiple statements. Use subqueries or CTEs if needed.")

    if not any(func in upper_query for func in AGGREGATE_FUNCTIONS) and not "LIMIT" in upper_query:
        raise ValueError("The generated SQL query should include a aggregate function or LIMIT clause to prevent excessive data retrieval.")
    
    from_tables = re.findall(rf"{re.escape("FROM")}\s+(\w+)", upper_query)
    for table in from_tables:
        if table not in TABLE_NAMES:
            raise ValueError(f"The generated SQL query references an unknown table: {table}")

    join_tables = re.findall(rf"{re.escape("JOIN")}\s+(\w+)", upper_query)
    for table in join_tables:
        if table not in TABLE_NAMES:
            raise ValueError(f"The generated SQL query references an unknown table: {table}")

    columns = re.findall(r"SELECT\s+(.*?)\s+FROM", upper_query, re.DOTALL)
    if columns:
        column_list = re.split(r',\s*', columns[0])
        for column in column_list:
            column_name = re.sub(r'\bAS\b.*', '', column, flags=re.IGNORECASE).strip()
            if not any(re.search(rf'\b{re.escape(col)}\b', column_name) for col in COLUMN_NAMES):
                raise ValueError(f"The generated SQL query references an unknown column: {column_name}")

    columns = re.findall(r"WHERE\s+(.*?)\s+", upper_query, re.DOTALL)
    if columns:
        column_list = re.split(r'\s+AND\s+|\s+OR\s+', columns[0])
        for column in column_list:
            column_name = re.split(r'[<>=!]+', column)[0].strip()
            if not any(re.search(rf'\b{re.escape(col)}\b', column_name) for col in COLUMN_NAMES):
                raise ValueError(f"The generated SQL query references an unknown column: {column_name}")

    return query

