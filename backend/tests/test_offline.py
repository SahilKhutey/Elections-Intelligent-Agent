from app.services.offline_service import get_offline_answer

def test_offline_match():
    result = get_offline_answer("How do I vote?", "en")
    assert result is not None
    assert "Register" in result

def test_offline_hindi():
    result = get_offline_answer("how to vote", "hi")
    assert result is not None
    assert "पंजीकरण" in result

def test_offline_no_match():
    result = get_offline_answer("random unrelated query", "en")
    assert result is None
