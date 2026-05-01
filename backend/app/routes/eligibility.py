from fastapi import APIRouter
from app.models.schemas import EligibilityRequest, EligibilityResponse
from app.services.translation_service import translation_service
from app.limiter import limiter
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/eligibility", response_model=EligibilityResponse)
@limiter.limit("10/minute")
def check_eligibility(request: Request, payload: EligibilityRequest):
    print(f"DEBUG: Eligibility Check for Age: {payload.age}, Citizen: {payload.is_citizen}, Resident: {payload.is_resident}")
    if not payload.is_citizen:
        message = "Only citizens are eligible to vote."
        return {
            "eligible": False,
            "message": translation_service.translate_text(message, payload.lang)
        }
    
    if not payload.is_resident:
        message = "Only residents are eligible to vote."
        return {
            "eligible": False,
            "message": translation_service.translate_text(message, payload.lang)
        }

    if payload.age >= 18:
        message = "You are eligible to vote."
        return {
            "eligible": True,
            "message": translation_service.translate_text(message, payload.lang)
        }

    message = f"You are not yet eligible to vote. You must be at least 18 years old. You will be eligible in {18 - payload.age} year(s)."
    return {
        "eligible": False,
        "message": translation_service.translate_text(message, payload.lang)
    }
