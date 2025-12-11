# 📚 Быстрая справка

## Быстый старт

```bash
cp .env.example .env
createdb telegram_logger
pip install -r requirements.txt
python main.py
```

## Получить данные

```python
# Search
await repo.search_messages(chat_id=123, text_query="Python")

# Stats
await repo.get_chat_statistics(123)
await repo.get_user_activity(123, days=7)

# Analytics
await analytics.get_top_users(123)
await analytics.get_chat_statistics(123)

# ML
await classifier.classify_intent("text")
await embeddings.find_similar_messages(query, messages)
await kg.get_user_expertise(user_id)
```

## Docker

```bash
docker-compose up -d
docker-compose logs -f
```
