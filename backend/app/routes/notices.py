from fastapi import APIRouter, HTTPException
from app.models.schemas import Notice, NoticeCreate
from app.config import settings
import json
import os
import uuid
from datetime import datetime
from typing import List

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/notices.json")

def load_notices():
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_notices(notices):
    with open(DATA_PATH, 'w') as f:
        json.dump(notices, f, indent=2)

@router.get("/notices", response_model=List[Notice])
def get_notices():
    return load_notices()

@router.post("/notices", response_model=Notice)
def create_notice(notice: NoticeCreate):
    if notice.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    notices = load_notices()
    new_notice = {
        "id": str(uuid.uuid4()),
        "title": notice.title,
        "content": notice.content,
        "type": notice.type,
        "timestamp": datetime.now().isoformat()
    }
    notices.insert(0, new_notice) # Add to top
    save_notices(notices)
    return new_notice
