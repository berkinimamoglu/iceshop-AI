from datetime import datetime
from typing import List, Literal, Optional, Dict
from pydantic import BaseModel


class FlashWindow(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str

    discount_percent: Optional[int] = None
    static_price: Optional[float] = None
    bundle_info: Optional[Dict] = None  # ileride yapılandırılabilir

    buyer_ids: List[str] = []
    pre_commit_ids: List[str] = []
    participant_ids: List[str] = []

    start_time: datetime
    end_time: datetime
    status: Literal["SCHEDULED", "ACTIVE", "EXPIRED"]
    product_id: Optional[str] = None
