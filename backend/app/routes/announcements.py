from fastapi import APIRouter, Query
from app.services.location_service import get_location_announcements
from typing import List, Dict, Any

router = APIRouter()

@router.get("/announcements")
async def get_announcements(location: str = Query("India", description="User's current location")):
    """
    Fetch location-aware announcements.
    """
    items = get_location_announcements(location)
    return {
        "location": location,
        "announcements": items,
        "count": len(items)
    }
