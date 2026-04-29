from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    location: Optional[str] = "general"
    lang: Optional[str] = "en"
    age: Optional[int] = None
    provider: str = "openai"
    api_key: Optional[str] = None

class QueryResponse(BaseModel):
    intent: str
    data: dict
    ai_response: str

class EligibilityRequest(BaseModel):
    age: int
    is_citizen: bool = True
    is_resident: bool = True
    lang: Optional[str] = "en"

class EligibilityResponse(BaseModel):
    eligible: bool
    message: str

class Notice(BaseModel):
    id: str
    title: str
    content: str
    type: str = "info" # info, urgent, success
    timestamp: str

class NoticeCreate(BaseModel):
    title: str
    content: str
    type: str = "info"
    password: str
