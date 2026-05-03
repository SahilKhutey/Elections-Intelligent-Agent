from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional, List, Any, Generic, TypeVar

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """Standardized API response format."""
    status: str = "success"
    data: T

class QueryRequest(BaseModel):
    """Schema for AI query requests."""
    query: str = Field(..., min_length=2, max_length=500, description="The user's election-related question.")
    lang: str = Field("en", pattern="^(en|hi)$", description="Language code (en or hi).")
    location: str = Field("India", min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=120)
    provider: str = Field("gemini", pattern="^(gemini|openai|anthropic)$")

    @field_validator('query')
    @classmethod
    def check_malicious_patterns(cls, v: str) -> str:
        # Basic Prompt Injection Protection
        blocked = ["ignore previous", "system prompt", "bypass", "jailbreak", "developer mode"]
        if any(p in v.lower() for p in blocked):
            raise ValueError("Query contains restricted patterns.")
        return v

class QueryResponse(BaseModel):
    """Schema for AI query responses."""
    intent: str
    data: Any
    ai_response: str

class EligibilityRequest(BaseModel):
    """Schema for voter eligibility check requests."""
    age: int = Field(..., ge=0, le=120)
    is_citizen: bool = True
    is_resident: bool = True
    lang: str = Field("en", pattern="^(en|hi)$")

class EligibilityResponse(BaseModel):
    """Schema for voter eligibility check responses."""
    eligible: bool
    message: str

class TimelineStep(BaseModel):
    """Schema for a single step in an election timeline."""
    stage: str
    date: str
    status: str

class TimelineResponse(BaseModel):
    """Schema for full timeline responses."""
    timeline: List[TimelineStep]

class NoticeCreate(BaseModel):
    """Schema for creating a new official notice."""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10, max_length=2000)
    type: str = Field("info", pattern="^(info|urgent|success)$")
    password: str # For admin validation

class NoticeResponse(BaseModel):
    """Schema for notice retrieval responses."""
    id: int
    title: str
    content: str
    type: str
    timestamp: str

class FAQItem(BaseModel):
    """Schema for a single FAQ entry."""
    question: str
    answer: str

class FAQResponse(BaseModel):
    """Schema for FAQ list responses."""
    faqs: List[FAQItem]

class EPICRequest(BaseModel):
    """Schema for EPIC verification requests."""
    epic: str = Field(..., pattern="^[A-Z]{3}\d{7}$", description="EPIC number (e.g. ABC1234567)")

class EPICResponse(BaseModel):
    """Schema for EPIC verification responses."""
    voter_name: str
    polling_station: str
    booth_number: str
    constituency: str
    district: str
    state: str
