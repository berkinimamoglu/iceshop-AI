from typing import List, Optional
from pydantic import BaseModel

from .location import Location


class Buyer(BaseModel):
    id: str
    phone_number: str
    name: Optional[str] = None
    location: Optional[Location] = None
    categories: List[str] = []
    price_sensitivity: Optional[str] = None  # "low" | "balanced" | "premium"
