from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

from app.core.campaign_logic import (
    analyze_ai_opportunities,
    create_seller_driven_campaign,
    process_buyer_driven_trigger
)

router = APIRouter()

# --------------------------
# Request Models
# --------------------------

class SellerCampaignRequest(BaseModel):
    seller_id: str
    product_id: str
    min_price: float
    max_price: float
    min_volume: int
    deadline: Optional[str] = None


class BuyerDemandTrigger(BaseModel):
    product_id: str
    buyer_demands: List[Dict]


# --------------------------
# Endpoints
# --------------------------

@router.post("/seller-create")
def seller_create_campaign(req: SellerCampaignRequest):
    """
    Seller-driven campaign creation skeleton
    """
    result = create_seller_driven_campaign(req)
    return {"status": "ok", "result": result}


@router.post("/buyer-trigger")
def buyer_trigger_campaign(req: BuyerDemandTrigger):
    """
    Buyer-driven trigger → system checks if threshold is met,
    if yes, forward to seller approval stage.
    """
    result = process_buyer_driven_trigger(req)
    return {"status": "ok", "result": result}


@router.get("/ai-scan")
def ai_scan():
    """
    AI-driven campaign opportunity scan.
    """
    opportunities = analyze_ai_opportunities()
    return {"status": "ok", "opportunities": opportunities}
