from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from typing import AsyncGenerator, Dict, Any
from app.models.schemas import QueryRequest
from app.services.ai_service import ai_service
from app.services.intent_service import intent_detector
from app.services.knowledge_service import knowledge_service
from app.services.translation_service import translation_service
from app.limiter import limiter

router = APIRouter()

async def stream_generator(payload: QueryRequest) -> AsyncGenerator[Dict[str, str], None]:
    """
    Simulates real-time typing by streaming the AI response word-by-word via SSE.
    
    Args:
        payload (QueryRequest): The user's query and metadata.
        
    Yields:
        Dict[str, str]: SSE event data containing response fragments.
    """
    # 1. Intent Detection & Knowledge Retrieval
    intent = intent_detector.detect_intent(payload.query)
    data = knowledge_service.get_election_process(payload.location) if intent == "voting_process" else \
           knowledge_service.get_timeline_template(payload.location) if intent == "timeline" else \
           knowledge_service.get_faq(intent)
    
    # 2. Multilingual Processing
    translated_data = translation_service.translate_response(data, payload.lang)
    
    # 3. AI Response Synthesis
    context = {
        'location': payload.location,
        'age': payload.age,
        'lang': payload.lang,
        'provider': payload.provider
    }
    
    full_text = ai_service.enhance_explanation(payload.query, translated_data, context)

    # 4. SSE Streaming Loop
    words = full_text.split()
    for word in words:
        yield {
            "event": "message",
            "data": word + " "
        }
        await asyncio.sleep(0.04) # Human-like typing cadence

    # 5. Signal Completion
    yield {
        "event": "message",
        "data": "[DONE]"
    }

@router.post("/stream")
@limiter.limit("5/minute")
async def stream_response(request: Request, payload: QueryRequest):
    """
    SSE Endpoint for real-time, interactive AI guidance.
    """
    return EventSourceResponse(stream_generator(payload))
