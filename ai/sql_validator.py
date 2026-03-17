import re

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

    if not upper_query.startswith("SELECT"):
        raise ValueError("The generated SQL query must contain a SELECT statement.")

    if re.search(r'\bSELECT\s+\*', upper_query):
        raise ValueError("The generated SQL query should not use SELECT *; please specify the columns explicitly.")

    if upper_query.count(";") > 1:
        raise ValueError("The generated SQL query shouldn't contain multiple statements. Use subqueries or CTEs if needed.")

    if not any(func in upper_query for func in AGGREGATE_FUNCTIONS) and not "LIMIT" in upper_query:
        raise ValueError("The generated SQL query should include a aggregate function or LIMIT clause to prevent excessive data retrieval.")

    return query

