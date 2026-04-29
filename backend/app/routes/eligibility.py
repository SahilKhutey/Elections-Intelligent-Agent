from fastapi import APIRouter
from app.models.schemas import EligibilityRequest, EligibilityResponse
from app.services.translation_service import translation_service

router = APIRouter()

@router.post("/eligibility", response_model=EligibilityResponse)
def check_eligibility(req: EligibilityRequest):
    print(f"DEBUG: Eligibility Check for Age: {req.age}, Citizen: {req.is_citizen}, Resident: {req.is_resident}")
    if not req.is_citizen:
        message = "Only citizens are eligible to vote."
        return {
            "eligible": False,
            "message": translation_service.translate_text(message, req.lang)
        }
    
    if not req.is_resident:
        message = "Only residents are eligible to vote."
        return {
            "eligible": False,
            "message": translation_service.translate_text(message, req.lang)
        }

    if req.age >= 18:
        message = "You are eligible to vote."
        return {
            "eligible": True,
            "message": translation_service.translate_text(message, req.lang)
        }

    message = f"You are not yet eligible to vote. You must be at least 18 years old. You will be eligible in {18 - req.age} year(s)."
    return {
        "eligible": False,
        "message": translation_service.translate_text(message, req.lang)
    }
