import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

class NoticeService:
    """
    Service for managing official election notices and announcements.
    Handles persistence and retrieval from static JSON stores.
    """
    def __init__(self, data_path: str = '../../data/notices.json'):
        self.data_path: str = os.path.normpath(os.path.join(os.path.dirname(__file__), data_path))
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w') as f:
                json.dump([], f)

    def load_notices(self) -> List[Dict[str, Any]]:
        """Loads all notices from the JSON store."""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading notices: {e}")
            return []

    def save_notice(self, title: str, content: str, notice_type: str) -> Dict[str, Any]:
        """
        Persists a new notice to the store.
        
        Args:
            title (str): Notice title.
            content (str): Notice body.
            notice_type (str): Type (info, urgent, etc).
            
        Returns:
            Dict[str, Any]: The newly created notice object.
        """
        notices = self.load_notices()
        new_notice = {
            "id": int(uuid.uuid4().int % 100000), # Short numeric ID for simplicity
            "title": title,
            "content": content,
            "type": notice_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        notices.insert(0, new_notice)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(notices, f, indent=2)
        return new_notice

# Singleton instance
notice_service = NoticeService()
