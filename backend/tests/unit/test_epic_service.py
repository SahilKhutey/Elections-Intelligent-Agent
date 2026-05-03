import pytest
from app.services.epic_service import epic_service

def test_epic_validation():
    """
    Verifies EPIC number format validation logic.
    """
    assert epic_service.validate("ABC1234567") is True
    assert epic_service.validate("XYZ9876543") is True
    assert epic_service.validate("123ABC4567") is False  # Wrong start
    assert epic_service.validate("ABC123456") is False   # Too short
    assert epic_service.validate("ABC12345678") is False # Too long

def test_epic_verification_mock():
    """
    Verifies that the service returns mock voter details for a valid EPIC.
    """
    details = epic_service.verify_and_fetch_details("ABC1234567")
    assert details is not None
    assert details["voter_name"] == "Rajesh Kumar"
    assert "booth_number" in details

def test_invalid_epic_verification():
    """
    Verifies that invalid EPIC numbers return None.
    """
    assert epic_service.verify_and_fetch_details("INVALID") is None
