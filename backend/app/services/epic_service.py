import re
from typing import Dict, Any, Optional

class EPICService:
    """
    Service for validating and verifying Election Photo Identity Card (EPIC) numbers.
    Simulates verification against a central voter database.
    """
    
    def __init__(self) -> None:
        # Standard EPIC pattern: 3 letters followed by 7 digits
        self.pattern = re.compile(r'^[A-Z]{3}\d{7}$')

    def validate(self, epic_number: str) -> bool:
        """Checks if the EPIC number format is valid."""
        return bool(self.pattern.match(epic_number.upper()))

    def verify_and_fetch_details(self, epic_number: str) -> Optional[Dict[str, Any]]:
        """
        Simulates fetching voter details from a database based on EPIC number.
        Returns voter details if found, else None.
        """
        if not self.validate(epic_number):
            return None
            
        # Mock data for demo purposes
        # In a real system, this would query a secure Election Commission API
        return {
            "voter_name": "Rajesh Kumar",
            "polling_station": "Govt Higher Secondary School, Sector 4",
            "booth_number": "42A",
            "constituency": "Bhopal North",
            "district": "Bhopal",
            "state": "Madhya Pradesh"
        }

# Singleton instance
epic_service = EPICService()
