from fastapi import APIRouter**

router = APIRouter()

@router.get("/sellers")
def list_sellers():
    return {"message": "Sellers list placeholder."}
