from fastapi import APIRouter

from backend.app.core.campaign_logic import analyze_ai_opportunities

router = APIRouter(tags=["campaigns"])


@router.get("/campaigns/opportunities")
async def get_ai_opportunities():
    """
    Alıcı ve satıcı sinyallerine göre AI fırsat analizi.
    Faz 1'de dummy (mock) sonuç döner.
    """
    return analyze_ai_opportunities()
