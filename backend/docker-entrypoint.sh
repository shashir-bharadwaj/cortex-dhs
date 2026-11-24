#!/bin/sh
# Container start-up for the Cortex backend image.
#   1. Apply database migrations.
#   2. Seed demo data according to SEED_MODE:
#        if-empty (default) - seed only when the users table has no rows (first run)
#        always             - reseed on every start (WIPES existing data)
#        never              - skip seeding
#   3. Start uvicorn.
set -e

echo "[entrypoint] Applying migrations..."
alembic upgrade head

SEED_MODE="${SEED_MODE:-if-empty}"
case "$SEED_MODE" in
  always)
    echo "[entrypoint] SEED_MODE=always -> reseeding database"
    python scripts/seed_dev_data.py
    ;;
  if-empty)
    USER_COUNT=$(python -c "
from sqlalchemy import text
from app.db.database import engine
with engine.connect() as c:
    print(c.execute(text('SELECT COUNT(*) FROM users')).scalar())
")
    if [ "$USER_COUNT" = "0" ]; then
      echo "[entrypoint] Empty database -> seeding demo data"
      python scripts/seed_dev_data.py
    else
      echo "[entrypoint] Database already has data ($USER_COUNT users) -> skipping seed"
    fi
    ;;
  never)
    echo "[entrypoint] SEED_MODE=never -> skipping seed"
    ;;
  *)
    echo "[entrypoint] Unknown SEED_MODE '$SEED_MODE' (use if-empty|always|never)" >&2
    exit 1
    ;;
esac

echo "[entrypoint] Starting API server on :8000"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers "${UVICORN_WORKERS:-1}"
