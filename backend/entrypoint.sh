#!/bin/sh
set -e

echo "[ENTRYPOINT] Running database setup..."
cd /app
python -c "
from app.core.database import engine, Base, SessionLocal
from app.main import create_default_user, seed_locations
from app.core.config import settings

Base.metadata.create_all(bind=engine)
if settings.DEBUG:
    create_default_user()
seed_locations()
print('[ENTRYPOINT] Setup complete.')
"

echo "[ENTRYPOINT] Starting Gunicorn..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120