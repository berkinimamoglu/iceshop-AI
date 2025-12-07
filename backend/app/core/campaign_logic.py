# app/core/campaign_logic.py

from typing import List, Dict
import random


# ---------------------------------------------------------
# MOCK DATA — ileride DB/Redis gelecek
# ---------------------------------------------------------

BUYERS = {}         # buyer state machine ile ilerleyecek
SELLERS = {}        # seller kayıtları
CAMPAIGNS = {}      # aktif & pending kampanyalar


# ---------------------------------------------------------
# SELLER-DRIVEN CAMPAIGN CREATION
# ---------------------------------------------------------

def create_seller_driven_campaign(req):
    """
    Skeleton: Seller kampanya açmak istediğinde burası çalışır.
    Bu sadece kampanya taslağını oluşturur.
    """
    campaign_id = f"CMP-{random.randint(1000,9999)}"

    CAMPAIGNS[campaign_id] = {
        "id": campaign_id,
        "type": "SELLER_DRIVEN",
        "seller_id": req.seller_id,
        "product_id": req.product_id,
        "min_price": req.min_price,
        "max_price": req.max_price,
        "min_volume": req.min_volume,
        "status": "WAITING_FOR_BUYERS",
        "collected_demand": []
    }

    return CAMPAIGNS[campaign_id]


# ---------------------------------------------------------
# BUYER-DRIVEN TRIGGER LOGIC
# ---------------------------------------------------------

def process_buyer_driven_trigger(req):
    """
    Eğer buyer taleği belirli bir threshold’a ulaşırsa
    sistemi seller onay aşamasına getirir.
    """
    total_volume = sum([d.get("volume", 1) for d in req.buyer_demands])

    # Skeleton threshold — ileride pricing & ML model eklenecek
    THRESHOLD = 10

    if total_volume >= THRESHOLD:
        return {
            "action": "ASK_SELLER_APPROVAL",
            "total_volume": total_volume,
            "product_id": req.product_id
        }

    return {
        "action": "KEEP_COLLECTING",
        "current_volume": total_volume,
        "threshold": THRESHOLD
    }


# ---------------------------------------------------------
# AI-DRIVEN OPPORTUNITY DETECTION
# ---------------------------------------------------------

def analyze_ai_opportunities() -> List[Dict]:
    """
    AI-driven skeleton:
    şu anda mock logic, ama gerçek sistemde burada:
    - buyer cluster analizi
    - seller stok fazlası tespiti
    - price curve analysis
    - ML scoring
    
    yapılacak.
    """
    mock_opportunity = {
        "seller_id": "S123",
        "product_id": "P900",
        "estimated_price": 95.0,
        "buyer_group": ["B001", "B004", "B033"],
        "score": 0.82,
        "action": "ASK_SELLER"
    }

    # ileride: Eğer gerçek fırsat yoksa boş liste dönecek
    return [mock_opportunity]
