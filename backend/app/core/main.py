from fastapi import FastAPI
from backend.app.api.v1.flash_window_routes import router as flash_window_router

app = FastAPI()

app.include_router(flash_window_router, prefix="/api/v1")
