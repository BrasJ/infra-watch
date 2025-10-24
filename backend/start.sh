#!/bin/sh
set -e

# Run migrations
alembic -c /code/backend/alembic.ini upgrade head

# Try both import paths for seeding (Render vs local)
if python -m app.seed_metrics 2>/dev/null; then
  echo "✅ Seeded using app.seed_metrics"
else
  python -m backend.app.seed_metrics && echo "✅ Seeded using backend.app.seed_metrics"
fi

# Launch FastAPI
if python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 2>/dev/null; then
  echo "🚀 Started using app.main"
else
  python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
fi
