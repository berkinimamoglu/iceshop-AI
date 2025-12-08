from fastapi import APIRouter

router = APIRouter()

@router.get("/campaigns")
def list_campaigns():
    return {"message": "List of campaigns will be added here."}

@router.post("/campaigns/create")
def create_campaign():
    return {"message": "Campaign creation endpoint placeholder."}
