from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime, timedelta

class SessionService:
    def __init__(self):
        self.sessions = {}
    
    def get_or_create(self, session_id: Optional[str] = None) -> str:
        if session_id and session_id in self.sessions:
            return session_id
        
        new_id = str(uuid.uuid4())
        self.sessions[new_id] = {
            'created_at': datetime.now(),
            'history': [],
            'context': {}
        }
        return new_id
    
    def add_history(self, session_id: str, query: str, response: str):
        if session_id in self.sessions:
            self.sessions[session_id]['history'].append({
                'q': query,
                'a': response[:200] # Truncate for memory efficiency
            })
            # Keep last 5 for context
            self.sessions[session_id]['history'] = self.sessions[session_id]['history'][-5:]

    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        if session_id in self.sessions:
            return self.sessions[session_id]['history']
        return []

session_service = SessionService()
