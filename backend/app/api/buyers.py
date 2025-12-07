from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

# --- In-memory "DB" (MVP için) ---
BUYERS: Dict[str, dict] = {}

# --- Request / Response Modelleri ---
class BuyerCreateRequest(BaseModel):
    whatsapp_id: str

class BuyerCreateResponse(BaseModel):
    whatsapp_id: str
    status: str


@router.post("/create", response_model=BuyerCreateResponse)
def create_buyer(payload: BuyerCreateRequest):
    """
    Yeni alıcı oluşturur.
    Aynı whatsapp_id daha önce geldiyse yeniden oluşturmaz.
    """
    whatsapp_id = payload.whatsapp_id.strip()

    if not whatsapp_id:
        raise HTTPException(status_code=400, detail="whatsapp_id cannot be empty")

    # Idempotent davranış
    if whatsapp_id in BUYERS:
        return BuyerCreateResponse(
            whatsapp_id=whatsapp_id,
            status="already_exists"
        )

    # Yeni alıcı oluştur
    BUYERS[whatsapp_id] = {
        "whatsapp_id": whatsapp_id,
        "state": "ASK_LOCATION",
        "data": {
            "location": None,
            "categories": None,
            "inventory": None,
            "availability": None
        }
    }

    return BuyerCreateResponse(
        whatsapp_id=whatsapp_id,
        status="created"
    )
