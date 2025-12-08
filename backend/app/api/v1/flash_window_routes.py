from fastapi import APIRouter
from app.core.campaign_logic import generate_flash_window

router = APIRouter()

@router.post("/flash-window/create")
async def create_flash_window(payload: dict):
    """
    Flash Purchase Window creation endpoint.
    """
    buyers = payload.get("buyers", [])
    seller = payload.get("seller", {})

    return generate_flash_window(
        buyer_group=buyers,
        seller_data=seller
    )
