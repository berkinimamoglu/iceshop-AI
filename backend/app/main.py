from fastapi import FastAPI

from app.api.buyers import router as buyers_router
from app.api.campaigns import router as campaigns_router

app = FastAPI(title="IceShop AI Backend")

app.include_router(buyers_router, prefix="/buyers", tags=["buyers"])
app.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])


@app.get("/")
def read_root():
    return {"message": "IceShop AI backend running"}
