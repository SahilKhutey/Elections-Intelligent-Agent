from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import NoticeCreate, NoticeResponse, StandardResponse
from app.services.notice_service import notice_service
from app.config import settings
from typing import List

router = APIRouter()

@router.get("/notices", response_model=StandardResponse[List[NoticeResponse]])
def get_notices():
    """
    Retrieves the list of all official notices.
    """
    notices = notice_service.load_notices()
    return {
        "status": "success",
        "data": notices
    }

@router.post("/notices", response_model=StandardResponse[NoticeResponse])
def create_notice(payload: NoticeCreate):
    """
    Creates a new official notice. Requires admin authentication.
    """
    if payload.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials.")
    
    new_notice = notice_service.save_notice(
        title=payload.title,
        content=payload.content,
        notice_type=payload.type
    )
    
    return {
        "status": "success",
        "data": new_notice
    }
