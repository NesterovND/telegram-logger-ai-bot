from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import logging

class ContextualEmbeddings:
    """Генерирует векторные представления сообщений"""
    
    def __init__(self, model_name: str = "distiluse-base-multilingual-cased-v2"):
        self.model = SentenceTransformer(model_name)
        self.logger = logging.getLogger(__name__)
        self.cache = {}
    
    async def embed_message(self, text: str) -> np.ndarray:
        """Онтять embedding для сообщения"""
        if text in self.cache:
            return self.cache[text]
        embedding = self.model.encode(text, convert_to_tensor=False)
        self.cache[text] = embedding
        return embedding
    
    async def find_similar_messages(
        self,
        query: str,
        messages: List[str],
        top_k: int = 5
    ) -> List[Dict]:
        """Найти похожие сообщения"""
        query_embedding = await self.embed_message(query)
        similarities = []
        
        for msg in messages:
            msg_embedding = await self.embed_message(msg)
            similarity = np.dot(query_embedding, msg_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(msg_embedding) + 1e-8
            )
            similarities.append({'text': msg, 'similarity': float(similarity)})
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:top_k]
    
    async def get_chat_context_vector(self, messages: List[str]) -> np.ndarray:
        """Получить целостный вектор контекста"""
        embeddings = [await self.embed_message(msg) for msg in messages]
        return np.mean(embeddings, axis=0)
