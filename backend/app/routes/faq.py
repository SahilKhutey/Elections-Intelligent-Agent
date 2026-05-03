from fastapi import APIRouter
from app.services.knowledge_service import knowledge_service
from app.models.schemas import FAQResponse, StandardResponse

router = APIRouter()

@router.get("/faq", response_model=StandardResponse[FAQResponse])
def get_faq(category: str = "general"):
    """
    Retrieves frequently asked questions for a specific category.
    """
    faqs = knowledge_service.get_faq(category)
    return {
        "status": "success",
        "data": {"faqs": faqs}
    }
