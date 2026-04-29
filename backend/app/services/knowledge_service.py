import json
import os
from typing import Dict, Any, Optional

class KnowledgeService:
    def __init__(self, data_dir: str = '../../data'):
        # Correct path for modular structure
        self.data_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), data_dir))
        self._load_data()
    
    def _load_data(self):
        """Load all static knowledge base files"""
        try:
            with open(f'{self.data_dir}/election_process.json', 'r') as f:
                self.election_process = json.load(f)
            with open(f'{self.data_dir}/timelines.json', 'r') as f:
                self.timelines = json.load(f)
            with open(f'{self.data_dir}/faq.json', 'r') as f:
                self.faq = json.load(f)
            with open(f'{self.data_dir}/eligibility.json', 'r') as f:
                self.eligibility = json.load(f)
        except Exception as e:
            print(f"Knowledge base loading warning: {e}")
            self.election_process = {"general": {}}
            self.timelines = {"general": {}}
            self.faq = {"general": {}}
            self.eligibility = {"rules": []}
    
    def get_election_process(self, location: str = 'general') -> Dict[str, Any]:
        return self.election_process.get(location, self.election_process.get('general', {}))
    
    def get_timeline_template(self, location: str = 'general') -> Dict[str, Any]:
        return self.timelines.get(location, self.timelines.get('general', {}))
    
    def get_faq(self, category: str = 'general') -> Dict[str, Any]:
        return self.faq.get(category, self.faq.get('general', {}))

    def get_eligibility_rules(self) -> Dict[str, Any]:
        return self.eligibility

# Singleton instance
knowledge_service = KnowledgeService()
