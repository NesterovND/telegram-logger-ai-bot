from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # === TELEGRAM API ===
    API_ID: int = os.getenv('API_ID')
    API_HASH: str = os.getenv('API_HASH')
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    
    # === DATABASE ===
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL',
        'postgresql+asyncpg://user:password@localhost:5432/telegram_logger'
    )
    
    # === LOGGING ===
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/bot.log')
    
    # === ML/AI ===
    ML_MODEL_BASE: str = os.getenv('ML_MODEL_BASE', 'mistralai/Mistral-7B')
    ML_TRAINING_INTERVAL: int = int(os.getenv('ML_TRAINING_INTERVAL', '21600'))  # 6 hours
    ML_MIN_MESSAGES_TO_TRAIN: int = int(os.getenv('ML_MIN_MESSAGES_TO_TRAIN', '1000'))
    ML_DEVICE: str = os.getenv('ML_DEVICE', 'cuda')
    
    # === FEATURES ===
    ENABLE_ML_TRAINING: bool = os.getenv('ENABLE_ML_TRAINING', 'true').lower() == 'true'
    ENABLE_KNOWLEDGE_GRAPH: bool = os.getenv('ENABLE_KNOWLEDGE_GRAPH', 'true').lower() == 'true'
    ENABLE_INTENT_CLASSIFICATION: bool = os.getenv('ENABLE_INTENT_CLASSIFICATION', 'true').lower() == 'true'
    ENABLE_AUTO_RESPONSE: bool = os.getenv('ENABLE_AUTO_RESPONSE', 'false').lower() == 'true'
    
    # === SERVER ===
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    
    class Config:
        env_file = '.env'

SETTINGS = Settings()
