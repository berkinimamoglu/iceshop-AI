from fastapi import APIRouter

from app.core.state import state
from app.core.campaign_logic import process_buyer_signal
from app.models.buyer import Buyer

router = APIRouter(prefix="/api/buyers", tags=["buyers"])


@router.post("/register")
def register_buyer(buyer: Buyer):
    state.add_buyer(buyer)
    return {"status": "ok", "buyer_id": buyer.id}


@router.post("/signal")
def buyer_signal(buyer_id: str, intent: str):
    buyer = state.get_buyer(buyer_id)
    if not buyer:
        return {"status": "error", "reason": "buyer_not_found"}

    process_buyer_signal(buyer, intent)
    return {"status": "ok"}
