import json
import os
from typing import List, Dict, Any

# Get absolute path to the data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "announcements.json")

def load_announcements() -> Dict[str, Any]:
    """Load announcements from the JSON file."""
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading announcements: {e}")
        return {}

def get_location_announcements(location: str) -> List[Dict[str, Any]]:
    """Get filtered announcements based on location."""
    data = load_announcements()
    results = []
    
    # Exact match (city-level or region-level)
    if location in data:
        results.extend(data[location])
    
    # Country fallback (India)
    if "India" in data and location != "India":
        # Add country-level info if not already there or as a supplement
        results.extend(data["India"])
    elif "India" in data and location == "India":
        results.extend(data["India"])
        
    return results[:4]  # Limit to 4 relevant items
