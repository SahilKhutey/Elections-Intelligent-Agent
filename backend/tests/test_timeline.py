def test_timeline_default(client):
    res = client.get("/api/timeline")

    assert res.status_code == 200
    data = res.json()
    assert "timeline" in data
    assert len(data["timeline"]) > 0

def test_timeline_hindi(client):
    res = client.get("/api/timeline?lang=hi")

    assert res.status_code == 200
    assert isinstance(res.json()["timeline"], list)
