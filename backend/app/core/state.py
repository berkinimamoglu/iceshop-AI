# app/core/state.py

from typing import Dict, Any

# ---------------------------------------------------------
# In-memory store (MVP)
# ---------------------------------------------------------

BUYERS: Dict[str, dict] = {}  # {whatsapp_id: {state: "", data: {...}}}


# ---------------------------------------------------------
# BASIC STATE ACCESSORS
# ---------------------------------------------------------

def get_buyer_state(whatsapp_id: str):
    return BUYERS.get(whatsapp_id)


def update_buyer_state(whatsapp_id: str, new_state: str, new_data: Dict[str, Any]):
    """
    Merges updated fields into buyer state
    """
    if whatsapp_id not in BUYERS:
        return

    BUYERS[whatsapp_id]["state"] = new_state
    BUYERS[whatsapp_id]["data"].update(new_data)



# ---------------------------------------------------------
# BASIC (STATIC) STATE MACHINE
# ileride AI + rules + scoring ile genişleyecek
# ---------------------------------------------------------

def determine_next_question(state: str):
    mapping = {
        "ASK_LOCATION":  "Hangi lokasyondasın?",
        "ASK_CATEGORIES": "Hangi kategoriler ilgini çekiyor?",
        "ASK_INVENTORY": "Ne kadar almak istersin?",
        "READY": "Talebini aldım. Teklifler hazır olduğunda bildireceğim.",
    }
    return mapping.get(state, "Bilgilerini güncellemek ister misin?")
