# 🚀 Развертывание на продакшене

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run bot
CMD ["python", "main.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: telegram_logger
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  bot:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@postgres:5432/telegram_logger
      API_ID: ${API_ID}
      API_HASH: ${API_HASH}
      BOT_TOKEN: ${BOT_TOKEN}
      ML_DEVICE: ${ML_DEVICE:-cpu}
    volumes:
      - ./logs:/app/logs
      - ./finetuned_models:/app/finetuned_models

volumes:
  postgres_data:
```

### Run
```bash
docker-compose up -d
```

## Kubernetes Deployment

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telegram-logger-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: telegram-logger-bot
  template:
    metadata:
      labels:
        app: telegram-logger-bot
    spec:
      containers:
      - name: bot
        image: your-registry/telegram-logger-bot:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: database-url
        - name: API_ID
          valueFrom:
            secretKeyRef:
              name: telegram-secrets
              key: api-id
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Linux Service (systemd)

### /etc/systemd/system/telegram-logger-bot.service
```ini
[Unit]
Description=Telegram Logger AI Bot
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/home/bot/telegram-logger-bot
Environment="PATH=/home/bot/telegram-logger-bot/venv/bin"
ExecStart=/home/bot/telegram-logger-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Включить
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-logger-bot
sudo systemctl start telegram-logger-bot
```

## Мониторинг

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

messages_processed = Counter('messages_processed_total', 'Total messages processed')
processing_time = Histogram('message_processing_seconds', 'Time to process message')
```

### Health Check
```python
@app.get("/health")
async def health_check():
    return {"status": "ok", "db": await check_db()}
```

## Backup Strategy

```bash
# Daily backup
0 2 * * * pg_dump telegram_logger | gzip > /backups/telegram_logger_$(date +\%Y\%m\%d).sql.gz

# Retention: 30 days
find /backups -name "telegram_logger_*.sql.gz" -mtime +30 -delete
```

## Performance Tuning

### PostgreSQL
```sql
-- Increase shared_buffers
shared_buffers = 256MB  -- for 4GB RAM

-- Enable parallel queries
max_parallel_workers_per_gather = 4

-- Better caching
effective_cache_size = 1GB
```

### Python
```bash
# Use uvloop for better async
pip install uvloop

# In main.py
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```
