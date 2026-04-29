import re
from typing import Dict, Any

class IntentDetectionService:
    def __init__(self):
        self.patterns = {
            'voting_process': [r'how.*vote', r'process', r'register', r'steps'],
            'timeline': [r'timeline', r'schedule', r'when', r'date', r'deadline'],
            'eligibility': [r'eligible', r'qualify', r'can.*vote', r'age'],
            'faq': [r'what', r'why', r'help', r'document', r'id']
        }
    
    def detect_intent(self, query: str) -> str:
        query_lower = query.lower()
        best_intent = "faq"
        max_matches = 0
        
        for intent, patterns in self.patterns.items():
            matches = sum(1 for p in patterns if re.search(p, query_lower))
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        
        return best_intent

intent_detector = IntentDetectionService()
