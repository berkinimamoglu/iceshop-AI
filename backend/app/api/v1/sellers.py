from typing import Dict, Any
from fastapi import APIRouter

from backend.app.core.campaign_logic import process_seller_signal

router = APIRouter(tags=["sellers"])


@router.post("/seller/trigger")
async def seller_trigger(payload: Dict[str, Any]):
    """
    Satıcı sinyali alan endpoint. Faz 1'de sadece memory'e yazar.
    """
    return process_seller_signal(payload)
