from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Message, User, Group
from datetime import datetime, timedelta
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class MessageRepository:
    """Работа с сообщениями в БД"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def save_message(self, message_data: dict):
        """Сохранить новое сообщение"""
        message = Message(**message_data)
        self.session.add(message)
        await self.session.commit()
        return message
    
    async def save_or_update_message(self, message_data: dict):
        """Сохранить или обновить сообщение"""
        existing = await self.session.execute(
            select(Message).where(
                and_(
                    Message.telegram_message_id == message_data['telegram_message_id'],
                    Message.telegram_chat_id == message_data['telegram_chat_id']
                )
            )
        )
        existing_msg = existing.scalars().first()
        
        if existing_msg:
            for key, value in message_data.items():
                setattr(existing_msg, key, value)
        else:
            existing_msg = Message(**message_data)
            self.session.add(existing_msg)
        
        await self.session.commit()
        return existing_msg
    
    async def search_messages(
        self,
        chat_id: Optional[int] = None,
        text_query: Optional[str] = None,
        sender_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Message]:
        """Поиск сообщений"""
        query = select(Message)
        conditions = []
        
        if chat_id:
            conditions.append(Message.telegram_chat_id == chat_id)
        if text_query:
            conditions.append(Message.text.ilike(f'%{text_query}%'))
        if sender_id:
            conditions.append(Message.telegram_sender_id == sender_id)
        if date_from:
            conditions.append(Message.message_date >= date_from)
        if date_to:
            conditions.append(Message.message_date <= date_to)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(desc(Message.message_date)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_user_activity(self, chat_id: int, days: int = 7):
        """Получить активность пользователей"""
        date_from = datetime.now() - timedelta(days=days)
        query = select(
            Message.sender_username,
            func.count(Message.id).label('message_count'),
            func.max(Message.message_date).label('last_message')
        ).where(
            and_(
                Message.telegram_chat_id == chat_id,
                Message.message_date >= date_from
            )
        ).group_by(Message.sender_username).order_by(desc('message_count'))
        
        result = await self.session.execute(query)
        return result.all()
    
    async def get_chat_statistics(self, chat_id: int) -> dict:
        """Получить статистику по чату"""
        result = await self.session.execute(
            select(
                func.count(Message.id).label('total_messages'),
                func.count(func.distinct(Message.sender_username)).label('unique_users'),
                func.min(Message.message_date).label('first_message'),
                func.max(Message.message_date).label('last_message')
            ).where(Message.telegram_chat_id == chat_id)
        )
        row = result.first()
        return {
            'total_messages': row[0] or 0,
            'unique_users': row[1] or 0,
            'first_message': row[2],
            'last_message': row[3]
        }
