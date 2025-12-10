from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    lng: float
    district: str
    neighborhood: str
