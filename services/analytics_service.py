from database.repositories.message_repo import MessageRepository
from datetime import datetime, timedelta
from typing import Dict
import logging

class AnalyticsService:
    """Аналитика сообщений"""
    
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)
    
    async def get_activity_timeline(self, chat_id: int, days: int = 30) -> Dict:
        """График активности"""
        date_from = datetime.now() - timedelta(days=days)
        activity = await self.message_repo.get_user_activity(chat_id, days)
        return {'activity': activity}
    
    async def get_top_users(self, chat_id: int, limit: int = 10):
        """Топ активных"""
        return await self.message_repo.get_user_activity(chat_id)
    
    async def get_chat_statistics(self, chat_id: int) -> Dict:
        """Общая статистика"""
        return await self.message_repo.get_chat_statistics(chat_id)
