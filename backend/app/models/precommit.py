from datetime import datetime
from pydantic import BaseModel


class PreCommit(BaseModel):
    id: str
    buyer_id: str
    seller_id: str
    proposed_window_id: str
    timestamp: datetime
