from typing import Dict, List, Set
import logging
from datetime import datetime
import json

class KnowledgeGraph:
    """Граф знаний из сообщений"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nodes = {}
        self.edges = {}
        self.user_profiles = {}
        self.logger.info("🔗 KnowledgeGraph инициализирован")
    
    async def extract_entities(self, text: str) -> List[str]:
        """Используя простые паттерны"""
        words = text.split()
        return [w for w in words if len(w) > 3]  # Фильтр коротких слов
    
    async def add_message_to_graph(self, message_id: int, text: str, sender_id: int):
        """Добавить инфо в граф"""
        entities = await self.extract_entities(text)
        
        for entity in entities:
            key = entity.lower()
            if key not in self.nodes:
                self.nodes[key] = {
                    'occurrences': 0,
                    'first_seen': datetime.now().isoformat(),
                    'mentioned_by': set()
                }
            
            self.nodes[key]['occurrences'] += 1
            self.nodes[key]['mentioned_by'].add(sender_id)
        
        if sender_id not in self.user_profiles:
            self.user_profiles[sender_id] = {
                'interests': {},
                'activity': 0
            }
        
        self.user_profiles[sender_id]['activity'] += 1
    
    async def get_user_expertise(self, user_id: int) -> Dict:
        """Получить экспертизу пользователя"""
        if user_id not in self.user_profiles:
            return {}
        
        profile = self.user_profiles[user_id]
        return {
            'activity_level': profile['activity'],
            'expertise_score': profile['activity']
        }
