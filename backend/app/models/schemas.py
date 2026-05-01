from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional

class QueryRequest(BaseModel):
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

class EligibilityRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    is_citizen: bool = True
    is_resident: bool = True
    lang: str = Field("en", pattern="^(en|hi)$")

class EligibilityResponse(BaseModel):
    eligible: bool
    message: str

class TimelineStep(BaseModel):
    stage: str
    date: str
    status: str

class NoticeCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10, max_length=2000)
    type: str = Field("info", pattern="^(info|urgent|success)$")
    password: str # For admin validation
