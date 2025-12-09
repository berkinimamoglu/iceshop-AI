from typing import Dict, Any
from fastapi import APIRouter

from backend.app.core.campaign_logic import process_buyer_signal

router = APIRouter(tags=["buyers"])


@router.post("/buyer/trigger")
async def buyer_trigger(payload: Dict[str, Any]):
    """
    Buyer, WhatsApp veya başka bir arayüzden sinyal gönderdiğinde
    ilk uğradığı endpoint. Faz 1'de sadece memory'e yazar.
    """
    return process_buyer_signal(payload)
