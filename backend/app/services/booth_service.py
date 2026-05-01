import json
import os
from typing import List, Dict

class BoothService:
    """
    Service for managing polling booth locations.
    """
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.abspath(os.path.join(current_dir, "..", "..", "data", "polling_booths.json"))
        self.booths = {}
        self._load_data()

    def _load_data(self):
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.booths = json.load(f)
        except Exception as e:
            print(f"Error loading booths: {e}")
            self.booths = {}

    def get_nearby_booths(self, location: str) -> List[Dict]:
        """
        Returns a list of booths for the specified city/location.
        """
        return self.booths.get(location, [])

booth_service = BoothService()
