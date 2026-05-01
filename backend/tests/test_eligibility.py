def test_eligible_user(client):
    res = client.post("/api/eligibility", json={
        "age": 20,
        "is_citizen": True,
        "is_resident": True
    })

    assert res.status_code == 200
    assert res.json()["eligible"] is True

def test_not_eligible_user(client):
    res = client.post("/api/eligibility", json={
        "age": 16,
        "is_citizen": True,
        "is_resident": True
    })

    assert res.json()["eligible"] is False

def test_invalid_citizenship(client):
    res = client.post("/api/eligibility", json={
        "age": 25,
        "is_citizen": False
    })

    assert res.json()["eligible"] is False
