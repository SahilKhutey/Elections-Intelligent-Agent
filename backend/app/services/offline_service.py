import json
import os
from typing import Optional

class OfflineService:
    """
    Backend implementation of the offline Q&A engine.
    Used for instant matching and as a fallback if AI services are down.
    """
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.abspath(os.path.join(current_dir, "..", "..", "data", "offline_qa.json"))
        self.db = {"how to vote": {"en": "Hardcoded Match"}}
        self._load_db()

    def _load_db(self):
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.db = json.load(f)
                print(f"DEBUG: Successfully loaded {len(self.db)} keys from {self.db_path}")
            else:
                print(f"DEBUG: Offline DB file NOT FOUND at {self.db_path}")
        except Exception as e:
            print(f"DEBUG: Error loading offline DB at {self.db_path}: {e}")
            self.db = {}

    def get_offline_answer(self, query: str, lang: str = "en") -> Optional[str]:
        """
        Performs robust word-level matching against the offline database.
        """
        import re
        # Clean query: lowercase and remove punctuation
        clean_q = re.sub(r'[^\w\s]', '', query.lower())
        q_words = set(clean_q.split())
        q_words = {w for w in q_words if len(w) > 2} # Keep words > 2 chars

        for key, answers in self.db.items():
            # Clean key
            clean_key = re.sub(r'[^\w\s]', '', key.lower())
            key_words = set(clean_key.split())
            key_words = {w for w in key_words if len(w) > 2}
            
            if q_words.intersection(key_words) or clean_key in clean_q:
                return answers.get(lang, answers.get("en"))
        
        return None

offline_service = OfflineService()

def get_offline_answer(query: str, lang: str = "en") -> Optional[str]:
    return offline_service.get_offline_answer(query, lang)
