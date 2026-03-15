from ai.schema_context import get_schema_prompt

def build_prompt_for_analytical_sql(user_query: str) -> str:
    prompt = """You are a data analyst.
            Your task is to generate analytical SQL queries for users questions.  
            """

    schema_prompt = get_schema_prompt()

    prompt += "\n\n" + schema_prompt

    prompt +=  """\n\nRules:
            - Never use SELECT *, always specify columns explicitly
            - Prefer aggregations (COUNT, SUM, AVG)
            - Return summarized data
            - Use LIMIT when returning lists"""

    prompt += f"\n\nUser Query: {user_query}\n\n"
    prompt += """Generate a SQL query that answers the user's question based on the provided database schema. 
                 Ensure the query follows the rules outlined above. 
                 Return only the SQL query without any explanations or additional text."""

    return prompt