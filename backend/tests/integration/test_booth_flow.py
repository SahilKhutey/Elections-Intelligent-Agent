import pytest

def test_booths_api(client):
    """
    Integration test for the /booths endpoint.
    """
    response = client.get("/api/booths?location=Bhopal")
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "booths" in json_data["data"]
    assert len(json_data["data"]["booths"]) > 0
    assert "location" in json_data["data"]

def test_epic_api_flow(client):
    """
    Integration test for the /epic verification endpoint.
    """
    # Valid EPIC
    response = client.post("/api/epic", json={"epic": "ABC1234567"})
    assert response.status_code == 200
    assert response.json()["data"]["voter_name"] == "Rajesh Kumar"
    
    # Invalid Format
    response = client.post("/api/epic", json={"epic": "INVALID"})
    assert response.status_code == 422 # Pydantic validation error
    
    # Not Found (correct format but not in mock DB - wait, my mock returns for all valid formats)
    # If I had a real DB, I'd test 404 here.
