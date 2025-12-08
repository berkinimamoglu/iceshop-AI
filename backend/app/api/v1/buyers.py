from fastapi import APIRouter

router = APIRouter()

@router.get("/buyers")
def list_buyers():
    return {"message": "Buyers list placeholder."}
