# backend/app/core/main.py

from fastapi import FastAPI

# Import routers
from backend.app.api.v1.buyers import router as buyer_router
from backend.app.api.v1.sellers import router as seller_router
from backend.app.api.v1.campaigns import router as campaign_router
from backend.app.api.v1.flash_window_routes import router as flash_window_router

app = FastAPI(
    title="Iceshop AI Backend",
    version="1.0.0"
)

# Register all routers
app.include_router(buyer_router, prefix="/api/v1")
app.include_router(seller_router, prefix="/api/v1")
app.include_router(campaign_router, prefix="/api/v1")
app.include_router(flash_window_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Iceshop backend running"}
