# 🤟 Contributing

## Development Setup

```bash
# Clone
git clone https://github.com/NesterovND/telegram-logger-ai-bot.git
cd telegram-logger-ai-bot

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
createdb telegram_logger

# Copy env
cp .env.example .env
# Edit with your credentials
```

## Code Style

- PEP 8 compliance
- Black for formatting
- Type hints required
- Docstrings for all functions

## Testing

```bash
pytest tests/ -v --cov
```

## PR Process

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

## Issues

Use GitHub Issues for:
- Bug reports
- Feature requests
- Questions

Include:
- Python version
- OS
- Error traceback
- Reproduction steps
