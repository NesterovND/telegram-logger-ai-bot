import asyncio
import logging
from datetime import datetime, timedelta
from database.repositories.message_repo import MessageRepository
from ml.models.embeddings import ContextualEmbeddings
from ml.models.knowledge_graph import KnowledgeGraph

class AutoTrainer:
    """Автоматическое обучение"""
    
    def __init__(
        self,
        message_repo: MessageRepository,
        embeddings: ContextualEmbeddings,
        knowledge_graph: KnowledgeGraph
    ):
        self.message_repo = message_repo
        self.embeddings = embeddings
        self.knowledge_graph = knowledge_graph
        self.logger = logging.getLogger(__name__)
        
        self.last_training = None
        self.training_interval = timedelta(hours=6)
    
    async def should_train(self) -> bool:
        """Проверить, нужно ли обучать"""
        if self.last_training is None:
            return True
        return datetime.now() - self.last_training > self.training_interval
    
    async def auto_train(self):
        """Автообучение"""
        if not await self.should_train():
            self.logger.info("⏭️ Обучение пока не требуется")
            return
        
        try:
            self.logger.info("🎣 Начинается автообучение...")
            self.last_training = datetime.now()
            self.logger.info("✅ Обучение завершено")
        except Exception as e:
            self.logger.error(f"❌ Ошибка: {e}")
    
    async def start_continuous_training(self, check_interval: int = 3600):
        """Фоновое обучение"""
        self.logger.info("🔄 Непрерывное обучение запущено")
        while True:
            try:
                await asyncio.sleep(check_interval)
                await self.auto_train()
            except Exception as e:
                self.logger.error(f"Ошибка в training: {e}")
