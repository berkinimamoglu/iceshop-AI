from fastapi import FastAPI

# DOĞRU IMPORT
from app.api.v1.buyers import router as buyers_router
from app.api.v1.sellers import router as sellers_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.flash_window_routes import router as flash_windows_router
from app.api.v1.whatsapp import router as whatsapp_router


app = FastAPI(title="Iceshop AI Backend")

# Routers
app.include_router(buyers_router)
app.include_router(sellers_router)
app.include_router(campaigns_router)
app.include_router(flash_windows_router)
app.include_router(whatsapp_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Iceshop AI Backend running"}
