from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import EPICRequest, EPICResponse, StandardResponse
from app.services.epic_service import epic_service
from app.limiter import limiter

router = APIRouter()

@router.post("/epic", response_model=StandardResponse[EPICResponse])
@limiter.limit("5/minute")
def verify_epic(request: Request, payload: EPICRequest):
    """
    Verifies an EPIC number and returns voter details.
    """
    voter_details = epic_service.verify_and_fetch_details(payload.epic)
    
    if not voter_details:
        raise HTTPException(
            status_code=404, 
            detail="EPIC number not found or invalid format."
        )
        
    return {
        "status": "success",
        "data": voter_details
    }
