# Setup

```bash
uv sync --dev
cp .env.example .env
uv run alembic -c alembic.ini upgrade head
uv run uvicorn app.main:app --reload
```
