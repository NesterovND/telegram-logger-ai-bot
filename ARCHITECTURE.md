# 🏡 Архитектура Telegram Logger AI Bot

## 📊 Общая схема системы

```
┌──────────────────────────────┐
│   TELEGRAM GROUP MESSAGES         │
└──────────────────────────────┘
           │
     ╯────╮
     │   │
     ╰────╮
     │   │
     ╰────╀

┌──────────────────────────────┐
│ TELETHON CLIENT (Multi-user API)  │
│   • Real-time listener             │
│   • Historical scanner             │
└──────────────────────────────┘
           │
           │ Raw message data
           │
           ━━━━━━━━╮
           │            │
           │            │
┌──────────────────────────────┐
│  MESSAGE HANDLER & STORAGE        │
│    • Metadata extraction           │
│    • Data validation               │
│    • DB persistence               │
└──────────────────────────────┘
           │
           │ Processed messages
           │
┌──────────────────────────────┐
│        POSTGRESQL DATABASE         │
│  │ Messages table                 │
│  │ Users table                    │
│  │ Groups table                   │
│  └ Statistics cache              │
└──────────────────────────────┘
           │
     ╯────╮
     │   │
     ╰────╮
     │   │
     ╰────╀

┌──────────────────────────────┐
│           ML/AI PIPELINE          │
│  ╯────────────────────────╮
│  │  Embeddings & Similarity     │
│  │  Intent Classification      │
│  │  Knowledge Graph Builder    │
│  │  Auto Response Generator    │
│  ╰────────────────────────╰
│              │
│  ╯────────────────────────╮
│  │  Auto-Training Loop (6h)   │
│  │  Incremental Fine-tuning   │
│  │  Model Checkpointing        │
│  ╰────────────────────────╰
└──────────────────────────────┘
           │
┌──────────────────────────────┐
│      ANALYTICS & INSIGHTS        │
│  • User profiles & expertise   │
│  • Activity statistics        │
│  • Entity relationships       │
└──────────────────────────────┘
```

## 📄 Поток данных

### 1. Real-time Processing
```
Telegram Message
    ↓
Telethon Listener
    ↓
Message Handler
    ↓
Extract: User, Chat, Text, Media, Metadata
    ↓
ML Processing:
    - Embed text
    - Classify intent
    - Extract entities
    - Update knowledge graph
    ↓
Store in PostgreSQL
```

### 2. Historical Scanning
```
Group/Channel
    ↓
Iter all messages backwards
    ↓
Batch process (100 at a time)
    ↓
ML enrichment
    ↓
Bulk insert/update
```

### 3. Auto-Training Loop
```
Every 6 hours OR 1000+ new messages
    ↓
Collect training data from DB
    ↓
Prepare dataset (Q&A pairs)
    ↓
Fine-tune model on GPU
    ↓
Save checkpoint
    ↓
Update knowledge graph
```

## 🖱️ Модель данных

### Groups
```
id               INTEGER PRIMARY KEY
telegram_chat_id INTEGER UNIQUE
title           STRING
username        STRING
is_channel      BOOLEAN
is_group        BOOLEAN
members_count   INTEGER
added_at        DATETIME
last_scanned_at DATETIME
```

### Users
```
id               INTEGER PRIMARY KEY
telegram_user_id INTEGER UNIQUE
username        STRING (indexed)
first_name      STRING
last_name       STRING
is_bot          BOOLEAN
first_seen_at   DATETIME
last_seen_at    DATETIME
message_count   INTEGER
```

### Messages (CORE TABLE)
```
id                   INTEGER PRIMARY KEY
telegram_message_id INTEGER (indexed)
group_id            INTEGER FK
sender_id           INTEGER FK
telegram_chat_id    INTEGER (indexed)
telegram_sender_id  INTEGER (indexed)
text                TEXT (indexed)
media_type          STRING
message_date        DATETIME (indexed)
received_at         DATETIME
is_edited           BOOLEAN

Composite Indexes:
- (chat_id, message_date)
- (sender_id, message_date)
```

### Statistics
```
id             INTEGER PRIMARY KEY
group_id       INTEGER FK
metric_name    STRING
metric_value   INTEGER
calculated_at  DATETIME
```

## 🤖 ML Pipeline

### Embeddings
- Model: `distiluse-base-multilingual-cased-v2`
- Dimension: 512
- Cache: in-memory for speed
- Use: semantic search, similarity

### Intent Classification
- question, statement, command, discussion, greeting, feedback
- Confidence scores for each
- Used for routing & analytics

### Knowledge Graph
- Nodes: entities (people, topics, projects)
- Edges: relationships
- User profiles: expertise, activity, interests
- Stored in JSON for fast access

### Training
- Base model: Mistral-7B (or smaller: GPT-2)
- Method: LoRA for efficient fine-tuning
- Input: (context, question) → (answer)
- Optimizer: AdamW with warmup
- Loss: CrossEntropyLoss with label smoothing

## 🌟 Масштабируемость

### Database
- Connection pooling: 20 connections
- Indexes on hot columns
- Materialized views for analytics
- Archiving old data

### ML Processing
- Batch processing (100 messages)
- GPU acceleration (CUDA)
- Model quantization (8-bit)
- Async/await throughout

### Async Architecture
- All I/O is non-blocking
- asyncio + asyncpg
- Can handle 1000s concurrent operations

## 🔐 Безопасность

- Environment variables for secrets
- SQL injection prevention (SQLAlchemy ORM)
- Input validation & sanitization
- Rate limiting ready
- No logs contain sensitive data

## 😋 Производительность

- Message ingestion: 100+ msg/sec
- Search latency: <100ms
- ML inference: <50ms per message
- Training time: 1-2 hours for 100k messages
- Memory: ~2GB base + model size
