from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from app.core.state import (
    BUYERS,
    get_buyer_state,
    update_buyer_state,
    determine_next_question
)

from app.core.prompts import ask_ai_for_next_step


router = APIRouter()

# --------------------------
# Request / Response Models
# --------------------------

class BuyerCreateRequest(BaseModel):
    whatsapp_id: str

class BuyerCreateResponse(BaseModel):
    whatsapp_id: str
    status: str


class BuyerAnswerRequest(BaseModel):
    whatsapp_id: str
    message: str   # buyer’ın WhatsApp cevabı (ör: “Beşiktaş”, “2 kilo”, “Kahve”)

class BuyerAnswerResponse(BaseModel):
    whatsapp_id: str
    next_state: str
    ai_reply: str
    updated_data: dict


# ---------------------------------------------------------
# CREATE BUYER
# ---------------------------------------------------------

@router.post("/create", response_model=BuyerCreateResponse)
def create_buyer(req: BuyerCreateRequest):
    if not req.whatsapp_id:
        raise HTTPException(status_code=400, detail="whatsapp_id required")

    if req.whatsapp_id in BUYERS:
        return BuyerCreateResponse(
            whatsapp_id=req.whatsapp_id,
            status="already_exists"
        )
    
    BUYERS[req.whatsapp_id] = {
        "state": "ASK_LOCATION",
        "data": {
            "location": None,
            "categories": [],
            "inventory": [],
        }
    }

    return BuyerCreateResponse(
        whatsapp_id=req.whatsapp_id,
        status="created"
    )


# ---------------------------------------------------------
# BUYER ANSWER: MAIN FLOW
# ---------------------------------------------------------

@router.post("/answer", response_model=BuyerAnswerResponse)
def answer_buyer(req: BuyerAnswerRequest):

    if req.whatsapp_id not in BUYERS:
        raise HTTPException(status_code=404, detail="Buyer not found")

    buyer = BUYERS[req.whatsapp_id]
    current_state = buyer["state"]

    # 1️⃣ AI’ye sor → bu mesajdan sonra ne yapmalıyım?
    ai_result = ask_ai_for_next_step(
        message=req.message,
        state=current_state,
        data=buyer["data"]
    )

    next_state = ai_result["next_state"]
    reply = ai_result["reply"]
    updated_data = ai_result["updated_data"]

    # 2️⃣ Backend state güncelle
    update_buyer_state(
        whatsapp_id=req.whatsapp_id,
        new_state=next_state,
        new_data=updated_data
    )

    return BuyerAnswerResponse(
        whatsapp_id=req.whatsapp_id,
        next_state=next_state,
        ai_reply=reply,
        updated_data=updated_data
    )
