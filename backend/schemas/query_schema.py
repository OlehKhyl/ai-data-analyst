from pydantic import BaseModel
from typing import List, Optional, Any

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    generated_sql: Optional[str] = None
    result: Optional[List[Any]] = None
    insight: Optional[str] = None

