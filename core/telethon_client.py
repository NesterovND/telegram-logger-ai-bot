from telethon import TelegramClient, events
from telethon.sessions import StringSession
import logging
from config.settings import SETTINGS

class TelethonClientManager:
    """Управление Telethon клиентом с поддержкой persistence"""
    
    def __init__(self):
        self.api_id = SETTINGS.API_ID
        self.api_hash = SETTINGS.API_HASH
        self.bot_token = SETTINGS.BOT_TOKEN
        self.client = None
        self.logger = logging.getLogger(__name__)
    
    async def init_client(self):
        """Инициализация и подключение клиента"""
        self.client = TelegramClient('bot_session', self.api_id, self.api_hash)
        await self.client.start(bot_token=self.bot_token)
        self.logger.info("✅ Telethon клиент инициализирован")
        return self.client
    
    async def get_groups_info(self):
        """Получить список всех групп/каналов где бот администратор"""
        dialogs = await self.client.get_dialogs()
        groups = [d for d in dialogs if d.is_group or d.is_channel]
        return groups
    
    async def disconnect(self):
        """Безопасное отключение"""
        if self.client:
            await self.client.disconnect()
