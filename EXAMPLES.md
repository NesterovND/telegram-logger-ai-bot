# 🚀 Примеры использования

## Базовое использование

### Запуск бота
```bash
python main.py
```

### Проверка логов
```bash
tail -f logs/bot.log
```

## Программное использование

### Получить статистику группы
```python
import asyncio
from database.connection import async_session
from database.repositories.message_repo import MessageRepository
from services.analytics_service import AnalyticsService

async def get_group_stats():
    async with async_session() as session:
        repo = MessageRepository(session)
        stats = await repo.get_chat_statistics(chat_id=123456)
        
        print(f"Total messages: {stats['total_messages']}")
        print(f"Unique users: {stats['unique_users']}")
        print(f"First message: {stats['first_message']}")
        print(f"Last message: {stats['last_message']}")

asyncio.run(get_group_stats())
```

### Найти активных пользователей
```python
async def get_top_users():
    async with async_session() as session:
        repo = MessageRepository(session)
        activity = await repo.get_user_activity(chat_id=123456, days=7)
        
        for username, count, last_msg in activity[:10]:
            print(f"{username}: {count} messages (last: {last_msg})")

asyncio.run(get_top_users())
```

### Поиск сообщений
```python
async def search_messages():
    async with async_session() as session:
        repo = MessageRepository(session)
        
        # Поиск по тексту
        messages = await repo.search_messages(
            chat_id=123456,
            text_query="Python",
            limit=20
        )
        
        for msg in messages:
            print(f"{msg.sender_username}: {msg.text}")
        
        # Поиск по пользователю
        user_messages = await repo.search_messages(
            chat_id=123456,
            sender_id=789,
            limit=50
        )
        
        # Поиск по диапазону дат
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        
        recent = await repo.search_messages(
            chat_id=123456,
            date_from=week_ago,
            limit=100
        )

asyncio.run(search_messages())
```

### Классификация интентов
```python
from ml.models.intent_classifier import IntentClassifier

async def classify_intent():
    classifier = IntentClassifier()
    
    texts = [
        "Привет, как дела?",
        "Когда будет релиз?",
        "/start",
        "Я согласен с этим предложением",
        "Спасибо за помощь!"
    ]
    
    for text in texts:
        result = await classifier.classify_intent(text)
        print(f"{text}")
        print(f"  Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print()

asyncio.run(classify_intent())
```

### Получить похожие сообщения
```python
from ml.models.embeddings import ContextualEmbeddings

async def find_similar():
    embeddings = ContextualEmbeddings()
    
    messages = [
        "Как установить Python?",
        "Что такое машинное обучение?",
        "Как начать с Django?",
        "Куда установить библиотеку?",
        "Что нужно для ML?"
    ]
    
    query = "Установка Python"
    similar = await embeddings.find_similar_messages(query, messages, top_k=3)
    
    print(f"Query: {query}")
    print("Similar messages:")
    for item in similar:
        print(f"  - {item['text']} (similarity: {item['similarity']:.2f})")

asyncio.run(find_similar())
```

### Knowledge Graph
```python
from ml.models.knowledge_graph import KnowledgeGraph

async def build_knowledge_graph():
    kg = KnowledgeGraph()
    
    # Добавить сообщения
    messages = [
        (1, "Я работаю с Python и Django", 101),
        (2, "Мне интересен Machine Learning", 101),
        (3, "Я разработчик на Go", 102),
        (4, "Python - мой любимый язык", 103),
    ]
    
    for msg_id, text, user_id in messages:
        await kg.add_message_to_graph(msg_id, text, user_id)
    
    # Получить экспертизу пользователя
    expertise = await kg.get_user_expertise(101)
    print(f"User 101 expertise: {expertise}")
    print(f"Topics: {kg.nodes}")

asyncio.run(build_knowledge_graph())
```

## REST API примеры

### FastAPI endpoints (если добавить)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/stats/{chat_id}")
async def get_stats(chat_id: int):
    stats = await analytics_service.get_chat_statistics(chat_id)
    return stats

@app.get("/api/search")
async def search(q: str, chat_id: int, limit: int = 50):
    results = await message_repo.search_messages(
        chat_id=chat_id,
        text_query=q,
        limit=limit
    )
    return {"results": results}

@app.get("/api/users/{chat_id}/top")
async def get_top_users(chat_id: int, limit: int = 10):
    users = await analytics_service.get_top_users(chat_id, limit)
    return {"users": users}
```

## Расширение функционала

### Добавить нотификации
```python
# services/notification_service.py

class NotificationService:
    async def notify_on_keyword(self, message, keywords):
        for keyword in keywords:
            if keyword.lower() in message.text.lower():
                await self.send_alert(message)
```

### Добавить модерацию
```python
# services/moderation_service.py

class ModerationService:
    async def check_message(self, message):
        if self.is_spam(message):
            return "spam"
        if self.is_toxic(message):
            return "toxic"
        return "ok"
```

### Добавить экспорт
```python
# services/export_service.py

class ExportService:
    async def export_to_csv(self, chat_id, file_path):
        messages = await self.message_repo.get_all_messages(chat_id)
        # Export logic...
    
    async def export_to_excel(self, chat_id, file_path):
        # Export with charts...
```

## Testing

```python
# tests/test_embeddings.py

import pytest
from ml.models.embeddings import ContextualEmbeddings

@pytest.mark.asyncio
async def test_embed_message():
    embeddings = ContextualEmbeddings()
    embed1 = await embeddings.embed_message("Hello world")
    embed2 = await embeddings.embed_message("Hello world")
    
    assert embed1.shape == (512,)
    assert (embed1 == embed2).all()  # Cache test

@pytest.mark.asyncio
async def test_find_similar():
    embeddings = ContextualEmbeddings()
    messages = [
        "Python programming",
        "Java development",
        "Python machine learning"
    ]
    
    similar = await embeddings.find_similar_messages(
        "Python ML",
        messages,
        top_k=2
    )
    
    assert len(similar) == 2
    assert similar[0]['text'] == "Python machine learning"
```
