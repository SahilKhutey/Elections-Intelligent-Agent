import re
from typing import Dict, List

class IntentDetectionService:
    """
    Lightweight rule-based service for detecting user intent from natural language queries.
    Uses regex patterns to classify queries into predefined categories.
    """
    def __init__(self):
        self.patterns: Dict[str, List[str]] = {
            'voting_process': [r'how.*vote', r'process', r'register', r'steps', r'procedure'],
            'timeline': [r'timeline', r'schedule', r'when', r'date', r'deadline', r'phases'],
            'eligibility': [r'eligible', r'qualify', r'can.*vote', r'age', r'requirement'],
            'faq': [r'what', r'why', r'help', r'document', r'id', r'card', r'voter.*id']
        }
    
    def detect_intent(self, query: str) -> str:
        """
        Classifies the query into one of the known intents based on keyword matching.
        
        Args:
            query (str): User's natural language input.
            
        Returns:
            str: The detected intent slug (e.g., 'voting_process', 'timeline').
        """
        query_lower = query.lower()
        best_intent = "faq"
        max_matches = 0
        
        for intent, patterns in self.patterns.items():
            matches = sum(1 for p in patterns if re.search(p, query_lower))
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        
        return best_intent

# Singleton instance for application-wide use
intent_detector = IntentDetectionService()
