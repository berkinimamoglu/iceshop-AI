# backend/app/core/campaign_logic.py

from typing import Dict, List
from backend.app.core.state import buyers, sellers, flash_windows
from backend.app.models.flash_window import FlashWindow


# ---------------------------------------------------------
# BUYER SIGNAL HANDLER
# ---------------------------------------------------------

def process_buyer_signal(payload: Dict) -> Dict:
    """
    Stores incoming buyer signal into in-memory state (Faz 1).
    """
    buyer_id = payload.get("buyer_id", "UNKNOWN")
    buyers.append(payload)

    return {
        "message": f"Buyer signal received from {buyer_id}",
        "total_buyers": len(buyers),
        "buyer_data": payload
    }


# ---------------------------------------------------------
# SELLER SIGNAL HANDLER
# ---------------------------------------------------------

def process_seller_signal(payload: Dict) -> Dict:
    """
    Stores incoming seller signal into in-memory state (Faz 1).
    """
    seller_id = payload.get("seller_id", "UNKNOWN")
    sellers.append(payload)

    return {
        "message": f"Seller signal received from {seller_id}",
        "total_sellers": len(sellers),
        "seller_data": payload
    }


# ---------------------------------------------------------
# AI-OPPORTUNITY ANALYZER (Faz 1 - Simulated)
# ---------------------------------------------------------

def analyze_ai_opportunities() -> List[Dict]:
    """
    Dummy AI opportunity logic (Faz 1).
    Returns a mocked opportunity for testing the system.
    """

    if not buyers or not sellers:
        return [{
            "status": "waiting",
            "reason": "Not enough buyers or sellers to generate opportunity."
        }]

    mock_opportunity = {
        "seller_id": sellers[-1].get("seller_id"),
        "product_id": buyers[-1].get("product_id"),
        "estimated_price": 95.0,
        "buyer_group": [b.get("buyer_id") for b in buyers[-3:]],  # last 3 buyers
        "score": 0.82,
        "action": "ASK_SELLER"
    }

    return [mock_opportunity]


# ---------------------------------------------------------
# FLASH WINDOW GENERATION (Faz 1 - Simulated)
# ---------------------------------------------------------

def generate_flash_window(buyer_group: List[Dict], seller_data: Dict) -> Dict:
    """
    Creates a FlashWindow object using basic static logic (Faz 1).
    """

    if not buyer_group or not seller_data:
        return {"error": "Missing buyer group or seller data."}

    fw = FlashWindow(
        seller_id=seller_data.get("seller_id"),
        product_id=seller_data.get("product_id", "UNKNOWN"),
        start_time="14:00",
        end_time="14:20",
        expected_buyers=len(buyer_group),
        benefit="10% discount for flash buyers"
    )

    flash_windows.append(fw.dict())

    return {
        "status": "flash_window_created",
        "flash_window": fw.dict()
    }
