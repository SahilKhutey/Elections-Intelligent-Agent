def test_empty_query(client):
    res = client.post("/api/query", json={
        "query": "",
        "lang": "en"
    })
    # Should be 422 because of our Pydantic min_length=2
    assert res.status_code == 422

def test_large_query(client):
    res = client.post("/api/query", json={
        "query": "vote " * 100,
        "lang": "en"
    })
    # Should be 200 or 422 if it exceeds max_length=500
    assert res.status_code in [200, 422]

def test_unsupported_language(client):
    res = client.post("/api/query", json={
        "query": "How to vote?",
        "lang": "fr"
    })
    # Should be 422 because of our Pydantic pattern regex
    assert res.status_code == 422
