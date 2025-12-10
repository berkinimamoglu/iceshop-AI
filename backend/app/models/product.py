from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: str
    seller_id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None       # "coffee", "food", "market", ...
    price: float
    stock: Optional[int] = None          # opsiyonel, kasap/market için önemli
    is_active: bool = True
