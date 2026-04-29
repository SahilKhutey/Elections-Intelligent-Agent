from fastapi import APIRouter
from app.services.knowledge_service import knowledge_service

router = APIRouter()

@router.get("/faq")
def get_faq(category: str = "general"):
    return {"faq": knowledge_service.get_faq(category)}
