import pytest
from unittest.mock import patch
from app.services.ai_service import ai_service

def test_ai_fallback_logic():
    """
    Verifies that the AI service correctly falls back to rule-based data 
    when the AI provider fails.
    """
    data = {"steps": ["Step 1: Register", "Step 2: Vote"]}
    context = {"lang": "en", "provider": "openai"}
    
    # Mocking the AI calls to fail
    with patch.object(ai_service, '_call_openai', side_effect=Exception("OpenAI Down")):
        response = ai_service.enhance_explanation("how to vote", data, context)
        
        # Should return the fallback message
        assert "information I found" in response

def test_ai_persona_synthesis():
    """
    Verifies that the prompt builder correctly adjusts persona based on age.
    """
    query = "can I vote"
    data = {}
    
    # Under 18 persona
    system_under, _ = ai_service._build_prompts(query, data, "en", 16, "India")
    assert "under 18" in system_under.lower()
    assert "encouraging" in system_under.lower()
    
    # Adult persona
    system_adult, _ = ai_service._build_prompts(query, data, "en", 25, "India")
    assert "eligible voter" in system_adult.lower()
    assert "actionable" in system_adult.lower()
