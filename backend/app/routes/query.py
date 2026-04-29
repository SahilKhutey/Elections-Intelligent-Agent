from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.intent_service import intent_detector
from app.services.knowledge_service import knowledge_service
from app.services.ai_service import ai_service
from app.services.session_service import session_service
from app.services.translation_service import translation_service

router = APIRouter()

@router.post("/query")
def handle_query(request: QueryRequest):
    # Step 1: Manage Session
    session_id = session_service.get_or_create() # Simplified for hackathon
    history = session_service.get_context(session_id)
    
    # Step 2: Detect Intent
    intent = intent_detector.detect_intent(request.query)
    
    # Step 3: Get Knowledge
    data = knowledge_service.get_election_process(request.location) if intent == "voting_process" else \
           knowledge_service.get_timeline_template(request.location) if intent == "timeline" else \
           knowledge_service.get_faq(intent)
    
    # Step 4: Translate
    translated_data = translation_service.translate_response(data, request.lang)
    
    # Step 5: AI Synthesis with History
    audience = "First-time voter" if request.age and request.age < 25 else "General public"
    context = {
        'location': request.location,
        'age': request.age,
        'lang': request.lang,
        'provider': request.provider
    }
    
    ai_response = ai_service.enhance_explanation(
        request.query, translated_data, context
    )
    
    # Step 6: Update History
    session_service.add_history(session_id, request.query, ai_response)

    return {
        "intent": intent,
        "data": translated_data,
        "ai_response": ai_response
    }
