from telethon import errors
import logging
from database.repositories.message_repo import MessageRepository
from datetime import datetime
from typing import Optional

class HistoryScanner:
    """Сканирование исторических сообщений"""
    
    def __init__(self, client, message_repo: MessageRepository):
        self.client = client
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)
    
    async def scan_group_history(
        self,
        group_id: int,
        limit: Optional[int] = None,
        start_date: Optional[datetime] = None
    ):
        """Сканировать всю историю группы"""
        try:
            entity = await self.client.get_entity(group_id)
            self.logger.info(f"📖 Начало сканирования: {entity.title}")
            
            messages_count = 0
            async for message in self.client.iter_messages(entity, limit=limit, reverse=False):
                if start_date and message.date < start_date:
                    continue
                
                sender = await message.get_sender() if message.sender_id else None
                
                message_data = {
                    'telegram_message_id': message.id,
                    'telegram_chat_id': entity.id,
                    'chat_title': getattr(entity, 'title', None),
                    'telegram_sender_id': sender.id if sender else None,
                    'sender_username': getattr(sender, 'username', None),
                    'sender_first_name': getattr(sender, 'first_name', None),
                    'sender_last_name': getattr(sender, 'last_name', None),
                    'text': message.text,
                    'is_edited': message.edit_date is not None,
                    'media_type': self._detect_media_type(message),
                    'reply_to_msg_id': message.reply_to_msg_id,
                    'message_date': message.date,
                    'received_at': datetime.now()
                }
                
                await self.message_repo.save_or_update_message(message_data)
                messages_count += 1
                
                if messages_count % 100 == 0:
                    self.logger.info(f"⏳ Обработано: {messages_count}")
            
            self.logger.info(f"✅ Готово. Всего: {messages_count}")
            return messages_count
        except Exception as e:
            self.logger.error(f"❌ Ошибка: {e}")
    
    def _detect_media_type(self, message):
        if message.photo: return 'photo'
        elif message.video: return 'video'
        elif message.document: return 'document'
        return None
