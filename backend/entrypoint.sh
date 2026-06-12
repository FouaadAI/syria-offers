#!/bin/sh
set -e

echo "[ENTRYPOINT] Running database setup..."
cd /app
python -c "
from sqlalchemy import inspect
from app.core.database import engine, Base, SessionLocal
from app.main import create_default_user, seed_locations
from app.core.config import settings

inspector = inspect(engine)
existing_tables = inspector.get_table_names()

if not existing_tables:
    Base.metadata.create_all(bind=engine)
    print('[ENTRYPOINT] Database initialized.')
else:
    print('[ENTRYPOINT] Tables already exist — skipping create_all().')

if settings.DEBUG:
    create_default_user()
seed_locations()
print('[ENTRYPOINT] Setup complete.')
"

echo "[ENTRYPOINT] Starting Gunicorn..."
# Workers=2 (4 cores but RAM-conscious); max-requests recycles workers to prevent
# memory leaks from Gemini calls; timeout 60s is plenty for async FastAPI.
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app \
    --bind 0.0.0.0:8000 \
    --timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 50