from typing import Optional, List
from pydantic import BaseModel
from app.models.location import Location

class Seller(BaseModel):
    id: str
    phone_number: str
    name: str
    category: str
    location: Location
    density_status: Optional[str] = None
    stock_status: Optional[str] = None
    product_ids: List[str] = []
