import json
import os
from typing import Dict, Any, Optional, List

class KnowledgeService:
    """
    Service responsible for loading and retrieving static knowledge base data.
    Acts as a lightweight data access layer for election-related information.
    """
    def __init__(self, data_dir: str = '../../data'):
        # Correct path for modular structure
        self.data_dir: str = os.path.normpath(os.path.join(os.path.dirname(__file__), data_dir))
        self.election_process: Dict[str, Any] = {}
        self.timelines: Dict[str, Any] = {}
        self.faq: Dict[str, Any] = {}
        self.eligibility: Dict[str, Any] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """
        Loads all static JSON knowledge base files from the data directory.
        Provides robust error handling and safe fallbacks.
        """
        files = {
            'election_process': 'election_process.json',
            'timelines': 'timelines.json',
            'faq': 'faq.json',
            'eligibility': 'eligibility.json'
        }
        
        for attr, filename in files.items():
            path = os.path.join(self.data_dir, filename)
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        setattr(self, attr, json.load(f))
                else:
                    print(f"Warning: Knowledge file {filename} not found at {path}")
                    setattr(self, attr, {"general": {}} if attr != 'eligibility' else {"rules": []})
            except Exception as e:
                print(f"Knowledge base loading error ({filename}): {e}")
                setattr(self, attr, {"general": {}} if attr != 'eligibility' else {"rules": []})
    
    def get_election_process(self, location: str = 'general') -> Dict[str, Any]:
        """Retrieves voting process steps for a specific location."""
        return self.election_process.get(location, self.election_process.get('general', {}))
    
    def get_timeline_template(self, location: str = 'general') -> List[Dict[str, Any]]:
        """Retrieves the election timeline template for a specific location."""
        return self.timelines.get(location, self.timelines.get('general', []))
    
    def get_faq(self, category: str = 'general') -> List[Dict[str, str]]:
        """Retrieves FAQ entries for a specific category."""
        return self.faq.get(category, self.faq.get('general', []))

    def get_eligibility_rules(self) -> Dict[str, Any]:
        """Retrieves global eligibility rules."""
        return self.eligibility

# Singleton instance for application-wide use
knowledge_service = KnowledgeService()
