# app/core/prompts.py

"""
Skeleton: Burada OpenAI API çağrısı yapacağız.
Şimdilik AI yanıtını simüle eden mock logic var.
"""

def ask_ai_for_next_step(message: str, state: str, data: dict):
    """
    AI’ye:
    - buyer state
    - buyer'ın verdiği mesaj
    - mevcut veri
    
    verilir ve AI:
    - hangi state'e geçileceğini
    - data'nın nasıl güncelleneceğini
    - buyer'a ne cevap yazılacağını

    belirler.

    Şimdilik MOCK, yarın API ile değişecek.
    """

    # MOCK STATE TRANSITION
    if state == "ASK_LOCATION":
        return {
            "next_state": "ASK_CATEGORIES",
            "reply": f"Tamamdır! Peki hangi ürün kategorileri ilgini çekiyor?",
            "updated_data": {
                "location": message
            }
        }

    if state == "ASK_CATEGORIES":
        return {
            "next_state": "ASK_INVENTORY",
            "reply": "Kaç adet veya ne kadar almak istersin?",
            "updated_data": {
                "categories": [message]
            }
        }

    if state == "ASK_INVENTORY":
        return {
            "next_state": "READY",
            "reply": "Harika! Talebini kaydettim. Yakında kampanyaları göndereceğim.",
            "updated_data": {
                "inventory": [message]
            }
        }

    # Default
    return {
        "next_state": "READY",
        "reply": "Bilgilerini aldım!",
        "updated_data": {}
    }
