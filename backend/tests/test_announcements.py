def test_announcements_default(client):
    res = client.get("/api/announcements")

    assert res.status_code == 200
    data = res.json()
    assert "announcements" in data

def test_announcements_location(client):
    res = client.get("/api/announcements?location=Bhopal")

    assert res.status_code == 200
    assert isinstance(res.json()["announcements"], list)
