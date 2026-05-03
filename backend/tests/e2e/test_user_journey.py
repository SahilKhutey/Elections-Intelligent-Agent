import pytest
from unittest.mock import patch
from app.services.ai_service import ai_service

def test_full_voter_journey(client):
    """
    E2E Test: Simulates a user journey with mocked AI for consistent results.
    """
    # Mock AI response to ensure it contains keywords the test looks for
    with patch.object(ai_service, '_generate_ai_response', return_value="Yes, you can vote if you are 18."):
        
        # Step 1: Initial Query
        res_query = client.post("/api/query", json={
            "query": "Can I vote if I am 18?",
            "location": "Bhopal",
            "lang": "en",
            "age": 18
        })
        assert res_query.status_code == 200
        response_text = res_query.json()["data"]["ai_response"].lower()
        assert "can" in response_text or "vote" in response_text

    # Step 2: Formal Eligibility Check
    res_eligibility = client.post("/api/eligibility", json={
        "age": 18,
        "is_citizen": True,
        "is_resident": True,
        "lang": "en"
    })
    assert res_eligibility.status_code == 200
    assert res_eligibility.json()["data"]["eligible"] is True

    # Step 3: Find Polling Booth
    res_booths = client.get("/api/booths?location=Bhopal")
    assert res_booths.status_code == 200
    assert len(res_booths.json()["data"]["booths"]) > 0

    # Step 4: Verify EPIC Card
    res_epic = client.post("/api/epic", json={"epic": "ABC1234567"})
    assert res_epic.status_code == 200
    assert "Rajesh" in res_epic.json()["data"]["voter_name"]

    # Step 5: Check Timeline
    res_timeline = client.get("/api/timeline?location=Bhopal")
    assert res_timeline.status_code == 200
    assert len(res_timeline.json()["data"]["timeline"]) > 0
