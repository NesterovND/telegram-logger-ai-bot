# 🚀 Telegram Logger AI Bot

> Профессиональный бот для экстракции и анализа всех сообщений в Telegram группе с ML/AI самообучением

## ✨ Основные возможности

### 📖 Отслеживание

✅ **Real-time monitoring** - похватывание всех новых сообщений  
✅ **Historical scanning** - сканирование всех старых сообщений до самого начала  
✅ **Complete metadata** - сохранение всего: кто, что, когда, куда, зачем, медиа, реплайы

### 🤖 ML/AI Компоненты

🔗 **Knowledge Graph** - отстроенные графы знаний из сообщений  
🟆 **Intent Classification** - определение типов сообщений (question, command, discussion, etc)  
🖍️ **Semantic Embeddings** - векторные представления для поиска по смыслу  
ඐ️ ↩️ **Auto Response Generation** - автоматическая генерация ответов  
📘 **User Expertise Profiles** - книжница экспертизы пользователей

### 🔄 Самообучение

🎣 **Incremental Learning** - непрерывное обучение на новых данных  
📄 **Fine-tuning** - энд-ту-энд дообучение моделей  
📊 **Analytics** - реальновременные статистики активности

## 📚 Архитектура

```
telegram-logger-ai-bot/
├── config/                 # Конфигурация
├── core/                  # Основные модули
├── database/              # Датабаза
├── ml/                    # ML/AI компоненты
├── services/              # Бизнес-логика
├── utils/                 # Утилиты
├── main.py                # точка входа
├── requirements.txt        # зависимости
└── .env.example           # настройки
```

## 🚀 Быстрый старт

### 1. Предпосылки

- Python 3.9+
- PostgreSQL 12+
- CUDA 11+ (для GPU ML)

### 2. Клонирование

```bash
git clone https://github.com/NesterovND/telegram-logger-ai-bot.git
cd telegram-logger-ai-bot
```

### 3. Настройка

```bash
# создать виртуальные энвранмент
 python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# установить зависимости
pip install -r requirements.txt

# настроить .env
cp .env.example .env
# Отредактируйте .env с вашими данными
```

### 4. Получение Telegram Credentials

1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Найдите **API_ID** и **API_HASH**
3. Создайте бота через @BotFather для **BOT_TOKEN**
4. Полните `.env`

### 5. Настройка PostgreSQL

```bash
# создать базу
creatdb telegram_logger
```

### 6. Запуск

```bash
python main.py
```

## 📊 Опции конфигурации

```env
# Telegram API
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/telegram_logger

# ML Features
ENABLE_ML_TRAINING=true              # включить/выключить обучение
ENABLE_KNOWLEDGE_GRAPH=true          # включить/выключить Knowledge Graph
ENABLE_INTENT_CLASSIFICATION=true    # классификация интентов
ENABLE_AUTO_RESPONSE=false           # автоматические ответы

ML_TRAINING_INTERVAL=21600           # интервал обучения (6 часов)
ML_MIN_MESSAGES_TO_TRAIN=1000        # минимум сообщений
ML_DEVICE=cuda                       # cuda или cpu
```

## 🎉 Модули

### `core/` - Основные компоненты

- **telethon_client.py** - управление Telethon клиентом
- **message_handler.py** - обработка новых сообщений
- **history_scanner.py** - сканирование истории

### `ml/` - ML/AI компоненты

- **models/** - модели ML
  - embeddings.py - семантические эмбеддинги
  - intent_classifier.py - классификатор интентов
  - knowledge_graph.py - граф знаний
- **training/** - тренинг
  - trainer.py - автоматическое обучение
- **generation/** - генерация
  - response_generator.py - генератор ответов

### `database/` - работа с БД

- **models.py** - SQLAlchemy модели
- **connection.py** - подключение к БД
- **repositories/** - работа с сущностями
  - message_repo.py - репозиторий сообщений

### `services/` - бизнес-логика

- analytics_service.py - аналитика и статистика

## 🛠️ Рассирите бота

Архитектура поддерживает легкое расширение:

```python
# Новые сервисы
services/notification_service.py   # уведомления
services/moderation_service.py    # модерация
services/export_service.py        # экспорт

# Новые ML модели
ml/models/sentiment_analyzer.py   # анализ тональности
ml/models/keyword_extractor.py    # экстракция ключевых слов

# API
api/routes/analytics.py           # рауты аналитики
api/routes/search.py              # поиск
```

## 🔅 Основные АПИ Сервиса

```python
# Получить статистику
stats = await analytics_service.get_chat_statistics(chat_id)

# Найти топ активных пользователей
top_users = await analytics_service.get_top_users(chat_id, limit=10)

# Поиск сообщений
messages = await message_repo.search_messages(
    chat_id=123,
    text_query="Python",
    limit=50
)

# Классифицировать интент
intent = await intent_classifier.classify_intent("Вы знаете Python?")

# Получить экспертизу пользователя
expertise = await knowledge_graph.get_user_expertise(user_id)
```

## 🐝 Отлаживание

```bash
# Включить детальные логи
LOG_LEVEL=DEBUG python main.py
```

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🤟 Помощь

Если у вас есть вопросы, открыте Issue вили придите Pull Request!
