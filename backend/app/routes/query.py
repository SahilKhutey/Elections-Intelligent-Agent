from fastapi import APIRouter, Request
from app.models.schemas import QueryRequest, QueryResponse, StandardResponse
from app.services.intent_service import intent_detector
from app.services.knowledge_service import knowledge_service
from app.services.ai_service import ai_service
from app.services.session_service import session_service
from app.services.translation_service import translation_service
from app.limiter import limiter

router = APIRouter()

@router.post("/query", response_model=StandardResponse[QueryResponse])
@limiter.limit("5/minute")
def handle_query(request: Request, payload: QueryRequest):
    """
    Main entry point for AI-powered election queries.
    Detects intent, retrieves relevant data, and synthesizes a response.
    """
    # Step 1: Manage Session
    session_id = session_service.get_or_create()
    
    # Step 2: Detect Intent
    intent = intent_detector.detect_intent(payload.query)
    
    # Step 3: Get Knowledge Base Data
    data = knowledge_service.get_election_process(payload.location) if intent == "voting_process" else \
           knowledge_service.get_timeline_template(payload.location) if intent == "timeline" else \
           knowledge_service.get_faq(intent)
    
    # Step 4: Translate Data to Target Language
    translated_data = translation_service.translate_response(data, payload.lang)
    
    # Step 5: AI Synthesis with Context
    context = {
        'location': payload.location,
        'age': payload.age,
        'lang': payload.lang,
        'provider': payload.provider
    }
    
    ai_response = ai_service.enhance_explanation(
        payload.query, translated_data, context
    )
    
    # Step 6: Persist History
    session_service.add_history(session_id, payload.query, ai_response)

    return {
        "status": "success",
        "data": {
            "intent": intent,
            "data": translated_data,
            "ai_response": ai_response
        }
    }
