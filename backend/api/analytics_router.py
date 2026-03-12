from fastapi import APIRouter
from backend.schemas.query_schema import QueryRequest, QueryResponse

router = APIRouter()

@router.post('/analytics/query', response_model=QueryResponse)
def query_analytics(request: QueryRequest) -> QueryResponse:
    # Placeholder for actual implementation
    generated_sql = "SELECT * FROM orders WHERE total_price > 100"
    result = [{"order_id": 1, "total_price": 150}, {"order_id": 2, "total_price": 200}]
    insight = "There are 2 orders with total price greater than 100."
    
    return QueryResponse(generated_sql=generated_sql, result=result, insight=insight)