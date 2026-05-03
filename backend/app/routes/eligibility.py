from fastapi import APIRouter, Request
from app.models.schemas import EligibilityRequest, EligibilityResponse, StandardResponse
from app.services.translation_service import translation_service
from app.limiter import limiter

router = APIRouter()

@router.post("/eligibility", response_model=StandardResponse[EligibilityResponse])
@limiter.limit("10/minute")
def check_eligibility(request: Request, payload: EligibilityRequest):
    """
    Calculates voter eligibility based on age, citizenship, and residency.
    """
    eligible = True
    message = ""

    if not payload.is_citizen:
        eligible = False
        message = "Only citizens are eligible to vote."
    elif not payload.is_resident:
        eligible = False
        message = "Only residents are eligible to vote."
    elif payload.age < 18:
        eligible = False
        message = f"You are not yet eligible to vote. You must be at least 18 years old. You will be eligible in {18 - payload.age} year(s)."
    else:
        message = "You are eligible to vote."

    return {
        "status": "success",
        "data": {
            "eligible": eligible,
            "message": translation_service.translate_text(message, payload.lang)
        }
    }
