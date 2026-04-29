from datetime import datetime, timedelta
from typing import List, Dict, Any
from .knowledge_service import knowledge_service

class TimelineEngine:
    def generate_timeline(self, location: str, start_date: str = None) -> List[Dict[str, Any]]:
        """Generate dynamic timeline with calculated dates"""
        template = knowledge_service.get_timeline_template(location)
        
        if not template:
            return []
        
        timeline = []
        current_date = datetime.now() if not start_date else datetime.fromisoformat(start_date)
        
        for i, stage in enumerate(template.get('stages', [])):
            duration_str = stage.get('status', '0 days') # Using status field as duration placeholder
            duration = self._parse_duration(duration_str)
            stage_date = current_date + duration
            
            timeline.append({
                'stage': stage['stage'],
                'status': stage.get('status', ''),
                'date': stage_date.strftime("%Y-%m-%d"),
                'is_active': i == 1 # Simulation
            })
            # Simplified for hackathon: current_date stays same for parallel stages
        
        return timeline

    def _parse_duration(self, duration_str: str) -> timedelta:
        try:
            if 'day' in duration_str.lower():
                days = int(duration_str.split()[0])
                return timedelta(days=days)
        except:
            pass
        return timedelta(0)

# Singleton instance
timeline_engine = TimelineEngine()
