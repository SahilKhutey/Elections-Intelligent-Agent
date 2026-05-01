from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.intent_service import intent_detector
from app.services.knowledge_service import knowledge_service
from app.services.ai_service import ai_service
from app.services.session_service import session_service
from app.services.translation_service import translation_service
from app.limiter import limiter
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/query")
@limiter.limit("5/minute")
def handle_query(request: Request, payload: QueryRequest):
    # Step 1: Manage Session
    session_id = session_service.get_or_create() # Simplified for hackathon
    history = session_service.get_context(session_id)
    
    # Step 2: Detect Intent
    intent = intent_detector.detect_intent(payload.query)
    
    # Step 3: Get Knowledge
    data = knowledge_service.get_election_process(payload.location) if intent == "voting_process" else \
           knowledge_service.get_timeline_template(payload.location) if intent == "timeline" else \
           knowledge_service.get_faq(intent)
    
    # Step 4: Translate
    translated_data = translation_service.translate_response(data, payload.lang)
    
    # Step 5: AI Synthesis with History
    audience = "First-time voter" if payload.age and payload.age < 25 else "General public"
    context = {
        'location': payload.location,
        'age': payload.age,
        'lang': payload.lang,
        'provider': payload.provider
    }
    
    ai_response = ai_service.enhance_explanation(
        payload.query, translated_data, context
    )
    
    # Step 6: Update History
    session_service.add_history(session_id, payload.query, ai_response)

    return {
        "intent": intent,
        "data": translated_data,
        "ai_response": ai_response
    }
