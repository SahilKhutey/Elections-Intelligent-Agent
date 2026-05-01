from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from app.services.ai_service import ai_service
from app.services.intent_service import intent_detector
from app.services.knowledge_service import knowledge_service
from app.services.translation_service import translation_service
from app.limiter import limiter

router = APIRouter()

async def stream_generator(query: str, lang: str, age: int, location: str):
    """
    Simulates real-time typing by streaming the AI response word-by-word.
    """
    # Step 1: Detect Intent & Get Knowledge (Fast)
    intent = intent_detector.detect_intent(query)
    data = knowledge_service.get_election_process(location) if intent == "voting_process" else \
           knowledge_service.get_timeline_template(location) if intent == "timeline" else \
           knowledge_service.get_faq(intent)
    
    # Step 2: Translate Knowledge
    translated_data = translation_service.translate_response(data, lang)
    
    # Step 3: Get Full AI Response (using the established ai_service)
    context = {
        'location': location,
        'age': age,
        'lang': lang,
        'provider': 'gemini' # Defaulting to Gemini for that "Powered by Google" feel
    }
    
    full_text = ai_service.enhance_explanation(query, translated_data, context)

    # Step 4: Stream word by word
    words = full_text.split()

    for word in words:
        yield {
            "event": "message",
            "data": word + " "
        }
        await asyncio.sleep(0.04)  # Natural typing speed

    yield {
        "event": "end",
        "data": "[DONE]"
    }

@router.post("/stream")
@limiter.limit("5/minute")
async def stream_response(request: Request):
    """
    SSE Endpoint for real-time AI responses.
    """
    body = await request.json()
    return EventSourceResponse(
        stream_generator(
            body.get("query"),
            body.get("lang", "en"),
            body.get("age"),
            body.get("location", "India")
        )
    )
