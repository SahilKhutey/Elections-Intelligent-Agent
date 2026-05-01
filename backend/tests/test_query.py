def test_query_basic(client):
    res = client.post("/api/query", json={
        "query": "How do I vote?",
        "lang": "en"
    })
    
    assert res.status_code == 200
    data = res.json()
    assert "ai_response" in data

def test_query_hindi(client):
    res = client.post("/api/query", json={
        "query": "मैं वोट कैसे करूं?",
        "lang": "hi"
    })

    assert res.status_code == 200
    assert isinstance(res.json()["ai_response"], str)

def test_query_with_personalization(client):
    res = client.post("/api/query", json={
        "query": "How to vote?",
        "lang": "en",
        "age": 20,
        "location": "Bhopal"
    })

    assert res.status_code == 200
