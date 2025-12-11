#!/usr/bin/env python3
"""
Telegram Logger AI Bot - Main Entry Point

🤖 Professional Telegram group message logger with self-learning AI capabilities
⚡ Real-time monitoring + Historical scanning
🖾 ML/AI for intent recognition, knowledge extraction, and auto-responses
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import SETTINGS
from utils.logger import setup_logging
from core.telethon_client import TelethonClientManager
from core.message_handler import MessageHandler
from core.history_scanner import HistoryScanner
from database.connection import init_db, async_session
from database.repositories.message_repo import MessageRepository

# ML Components
from ml.models.embeddings import ContextualEmbeddings
from ml.models.intent_classifier import IntentClassifier
from ml.models.knowledge_graph import KnowledgeGraph
from ml.training.trainer import AutoTrainer
from ml.generation.response_generator import ResponseGenerator

# Services
from services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

class TelegramLoggerBot:
    """Основной класс бота"""
    
    def __init__(self):
        self.telethon_manager = None
        self.client = None
        self.message_repo = None
        self.message_handler = None
        self.history_scanner = None
        self.auto_trainer = None
        self.response_generator = None
        self.analytics_service = None
    
    async def initialize(self):
        """Инициализация всех компонентов"""
        
        logger.info("="*60)
        logger.info("🚀 Запуск Telegram Logger AI Bot")
        logger.info("="*60)
        
        # 1. Инициализировать БД
        logger.info("💾 Инициализация базы данных...")
        await init_db()
        
        # 2. Открыть сессию
        async with async_session() as session:
            self.message_repo = MessageRepository(session)
            
            # 3. Инициализировать Telethon
            logger.info("🚀 Коннектинг к Telegram...")
            self.telethon_manager = TelethonClientManager()
            self.client = await self.telethon_manager.init_client()
            
            # 4. ML компоненты
            logger.info("🤖 Инициализация ML модулей...")
            embeddings = ContextualEmbeddings()
            intent_classifier = IntentClassifier()
            knowledge_graph = KnowledgeGraph()
            self.response_generator = ResponseGenerator()
            
            # 5. Сервисы
            self.analytics_service = AnalyticsService(self.message_repo)
            
            # 6. Обработчики и трейнер
            self.message_handler = MessageHandler(self.client, self.message_repo)
            self.history_scanner = HistoryScanner(self.client, self.message_repo)
            
            self.auto_trainer = AutoTrainer(
                message_repo=self.message_repo,
                embeddings=embeddings,
                knowledge_graph=knowledge_graph
            )
            
            logger.info("✅ Все компоненты открыты")
    
    async def run(self):
        """Показ бота"""
        
        await self.initialize()
        
        # Запустить слушание сообщений
        await self.message_handler.start_listening()
        
        # Начать непрерывное обучение
        if SETTINGS.ENABLE_ML_TRAINING:
            training_task = asyncio.create_task(
                self.auto_trainer.start_continuous_training(check_interval=3600)
            )
        
        # Получить группы
        groups = await self.telethon_manager.get_groups_info()
        logger.info(f"📖 Найдено групп: {len(groups)}")
        
        # Основной цикл
        try:
            logger.info("\n" + "="*60)
            logger.info("✅ Бот готов к работе!")
            logger.info("🔘 Ожидание сообщений...")
            logger.info("="*60 + "\n")
            
            await self.client.run_until_disconnected()
        
        except KeyboardInterrupt:
            logger.info("\n⚠️  Бот остановлен")
        
        finally:
            await self.telethon_manager.disconnect()

async def main():
    bot = TelegramLoggerBot()
    await bot.run()

if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
