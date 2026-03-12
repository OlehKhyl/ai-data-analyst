from fastapi import FastAPI
from backend.api.analytics_router import router as analytics_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Data Analyst API running"}


app.include_router(analytics_router)