from telethon import events
from datetime import datetime
import logging
from database.repositories.message_repo import MessageRepository

class MessageHandler:
    """Обработчик новых сообщений в реальном времени"""
    
    def __init__(self, client, message_repo: MessageRepository):
        self.client = client
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)
    
    async def start_listening(self):
        """Запустить слушание сообщений"""
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            try:
                await self._process_message(event)
            except Exception as e:
                self.logger.error(f"❌ Ошибка при обработке: {e}")
        
        self.logger.info("🆕 Слушание новых сообщений запущено")
    
    async def _process_message(self, event):
        """Обработка одного сообщения"""
        message = event.message
        chat = await event.get_chat()
        sender = await event.get_sender() if event.sender_id else None
        
        message_data = {
            'telegram_message_id': message.id,
            'telegram_chat_id': chat.id,
            'chat_title': getattr(chat, 'title', None),
            'telegram_sender_id': sender.id if sender else None,
            'sender_username': getattr(sender, 'username', None),
            'sender_first_name': getattr(sender, 'first_name', None),
            'sender_last_name': getattr(sender, 'last_name', None),
            'text': message.text,
            'is_edited': message.edit_date is not None,
            'media_type': self._detect_media_type(message),
            'media_file_id': self._get_media_id(message),
            'reply_to_msg_id': message.reply_to_msg_id,
            'message_date': message.date,
            'received_at': datetime.now()
        }
        
        await self.message_repo.save_message(message_data)
        self.logger.debug(f"💾 Сохранено: {message.id}")
    
    def _detect_media_type(self, message):
        if message.photo: return 'photo'
        elif message.video: return 'video'
        elif message.document: return 'document'
        elif message.audio: return 'audio'
        elif message.voice: return 'voice'
        return None
    
    def _get_media_id(self, message):
        if message.photo: return message.photo.id
        elif message.document: return message.document.id
        return None
