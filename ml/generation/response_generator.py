import logging
from typing import List

class ResponseGenerator:
    """Генератор ответов"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def generate_response(
        self,
        context: str,
        user_query: str,
        similar_messages: List[str] = None,
        max_length: int = 200
    ) -> str:
        """Генерировать ответ"""
        prompt = self._build_prompt(context, user_query, similar_messages)
        self.logger.info(f"🤖 Генерирую ответ на: {user_query}")
        return f"Response to: {user_query}"
    
    def _build_prompt(self, context: str, query: str, similar_messages: List[str] = None) -> str:
        prompt = f"Context: {context}\n"
        if similar_messages:
            prompt += "Similar: \n"
            for msg in similar_messages[:3]:
                prompt += f"  - {msg}\n"
        prompt += f"Query: {query}\nAnswer:"
        return prompt
