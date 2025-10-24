# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev python3-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /code/backend

EXPOSE 8000
CMD ["sh", "-c", "alembic -c /code/backend/alembic.ini upgrade head && python -m app.seed_metrics && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
