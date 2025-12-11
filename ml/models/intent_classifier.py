import torch
from typing import Dict
import logging

class IntentClassifier:
    """Классификация интентов сообщений"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.intents = {
            0: 'question',
            1: 'statement',
            2: 'command',
            3: 'discussion',
            4: 'greeting',
            5: 'feedback',
        }
        self.logger.info("🤖 IntentClassifier инициализирован")
    
    async def classify_intent(self, text: str) -> Dict:
        """Классифицировать интент"""
        # Простая гевристика для демо
        if text.strip().endswith('?'):
            intent = 'question'
            confidence = 0.95
        elif text.startswith('/'):
            intent = 'command'
            confidence = 0.98
        elif text.lower().startswith(('hi', 'дравствуй', 'hello', 'привет')):
            intent = 'greeting'
            confidence = 0.9
        else:
            intent = 'statement'
            confidence = 0.8
        
        return {
            'intent': intent,
            'confidence': confidence,
            'all_scores': {k: 0.1 for k in self.intents.values()}
        }
