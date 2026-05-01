from fastapi import APIRouter, Query
from app.services.booth_service import booth_service

router = APIRouter()

@router.get("/booths")
def get_booths(location: str = Query("Bhopal", description="City to fetch booths for")):
    """
    API endpoint to fetch polling booths for a given city.
    """
    booths = booth_service.get_nearby_booths(location)
    return {
        "status": "success",
        "location": location,
        "count": len(booths),
        "booths": booths
    }
