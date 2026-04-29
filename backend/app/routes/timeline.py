from fastapi import APIRouter
from app.services.timeline_service import timeline_engine

router = APIRouter()

@router.get("/timeline")
def get_timeline(lang: str = "en", location: str = "India"):
    timeline_data = timeline_engine.generate_timeline(location)
    # The engine currently returns a list of stages
    return {"timeline": timeline_data}
