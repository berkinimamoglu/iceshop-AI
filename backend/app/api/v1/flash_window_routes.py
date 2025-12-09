from typing import Dict, Any, List
from fastapi import APIRouter

from backend.app.core.campaign_logic import generate_flash_window

router = APIRouter(tags=["flash-window"])


@router.post("/flash-window/create")
async def create_flash_window(payload: Dict[str, Any]):
    """
    Mock AI fırsatına göre flash purchase window oluşturur.
    Faz 1'de sabit saat ve basit benefit ile döner.
    """
    buyers: List[Dict[str, Any]] = payload.get("buyers", [])
    seller: Dict[str, Any] = payload.get("seller", {})

    return generate_flash_window(
        buyer_group=buyers,
        seller_data=seller,
    )
