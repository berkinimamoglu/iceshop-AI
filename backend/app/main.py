from fastapi import FastAPI

from app.api.buyers import router as buyers_router

app = FastAPI(title="Project ICE API")

app.include_router(buyers_router, prefix="/buyers", tags=["buyers"])

@app.get("/")
def read_root():
    return {"message": "FastAPI application is running"}
