#!/bin/sh
set -e

echo "🚀 Starting backend setup..."

# Run Alembic migrations (safe to re-run)
echo "📦 Running database migrations..."
alembic -c /code/backend/alembic.ini upgrade head

# Check if hosts table already has data
echo "🔍 Checking if database already seeded..."
HOST_COUNT=$(psql "$DATABASE_URL" -tAc "SELECT COUNT(*) FROM hosts;" 2>/dev/null || echo 0)

if [ "$HOST_COUNT" -eq 0 ]; then
  echo "🌱 Seeding database (no existing hosts found)..."

  # Try both import paths for seeding
  if python -m app.seed_metrics 2>/dev/null; then
    echo "✅ Seeded using app.seed_metrics"
  else
    python -m backend.app.seed_metrics && echo "✅ Seeded using backend.app.seed_metrics"
  fi
else
  echo "⏩ Database already contains data ($HOST_COUNT hosts) — skipping seeding."
fi

# Start the FastAPI server
echo "🚀 Launching API service..."

if python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 2>/dev/null; then
  echo "✅ Started using app.main"
else
  python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
fi
