from fastapi import APIRouter, Query
from app.services.booth_service import booth_service
from app.models.schemas import StandardResponse
from typing import List, Dict, Any

router = APIRouter()

@router.get("/booths", response_model=StandardResponse[Dict[str, Any]])
def get_booths(location: str = Query("Bhopal", description="City to fetch polling booths for")):
    """
    Retrieves nearby polling booths for a specified location.
    """
    booths = booth_service.get_nearby_booths(location)
    return {
        "status": "success",
        "data": {
            "location": location,
            "count": len(booths),
            "booths": booths
        }
    }
