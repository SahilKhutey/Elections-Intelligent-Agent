import pytest
import time
from unittest.mock import patch
from app.services.ai_service import ai_service

def test_api_performance_latency(client):
    """
    Performance Test: Ensures the /booths API responds within a reasonable time.
    """
    start_time = time.time()
    response = client.get("/api/booths?location=Bhopal")
    end_time = time.time()
    
    duration = end_time - start_time
    assert response.status_code == 200
    assert duration < 0.5  # Expecting sub-500ms for static/cached data

def test_ai_failure_fallback_integration(client):
    """
    Failure Simulation: Ensures the API still returns a valid response 
    when the AI provider is completely down.
    """
    payload = {
        "query": "How to vote?",
        "location": "Bhopal",
        "lang": "en",
        "age": 25
    }
    
    # Simulate total failure of all AI providers in AIService
    with patch.object(ai_service, '_generate_ai_response', side_effect=Exception("API Connection Lost")):
        response = client.post("/api/query", json=payload)
        
        assert response.status_code == 200
        json_data = response.json()
        # Should contain the fallback text from AIService._fallback_response
        assert "information I found" in json_data["data"]["ai_response"]
