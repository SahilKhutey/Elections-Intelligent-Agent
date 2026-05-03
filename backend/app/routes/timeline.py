from fastapi import APIRouter
from app.services.timeline_service import timeline_engine
from app.models.schemas import TimelineResponse, StandardResponse

router = APIRouter()

@router.get("/timeline", response_model=StandardResponse[TimelineResponse])
def get_timeline(lang: str = "en", location: str = "India"):
    """
    Returns the election timeline for a specific location and language.
    """
    timeline_data = timeline_engine.generate_timeline(location)
    return {
        "status": "success",
        "data": {"timeline": timeline_data}
    }
