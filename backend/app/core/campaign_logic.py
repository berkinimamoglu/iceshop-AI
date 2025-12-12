from app.core.state import state
from app.models.buyer import Buyer
from app.models.seller import Seller


def process_buyer_signal(buyer: Buyer, intent: str):
    """
    Örnek logic: Buyer sinyallerini kaydet veya kampanya tetikle.
    Gerçek AI logic ileride gelecek.
    """
    print(f"[SIGNAL] Buyer {buyer.id} intent received:", intent)
    # burada daha gelişmiş scoring ve kampanya tetikleme ileride olacak
    return True


def evaluate_campaign_opportunity(seller: Seller):
    """
    AI fırsat motorunun temel skeleton'u.
    Şimdilik sadece log basıyor.
    """
    print(f"[AI] Evaluating opportunity for seller:", seller.id)
    # burada: lokasyon, pre-commit, yoğunluk, ürün vb. analiz edilecek
    return None
