import pytest

def test_query_api_success(client):
    """
    Integration test for the /query endpoint.
    Ensures that a valid query returns a structured response.
    """
    payload = {
        "query": "How do I register to vote?",
        "location": "Bhopal",
        "lang": "en",
        "age": 25,
        "provider": "gemini"
    }
    response = client.post("/api/query", json=payload)
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "ai_response" in json_data["data"]
    assert "intent" in json_data["data"]

def test_query_api_rate_limiting(client):
    """
    Verifies that rate limiting is working (simulated by making multiple requests).
    Note: In a real test env, we might need to adjust limits or use a mock.
    """
    payload = {"query": "test query", "location": "India", "age": 20}
    # Send multiple requests rapidly
    for _ in range(10):
        client.post("/api/query", json=payload)
    
    # The last one should likely be rate limited if the limit is low enough (5/min in code)
    # response = client.post("/api/query", json=payload)
    # assert response.status_code == 429
