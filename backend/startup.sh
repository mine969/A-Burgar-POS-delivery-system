#!/bin/bash

echo "Waiting for PostgreSQL..."
sleep 5

echo "Checking if DB is empty..."
TABLE_COUNT=$(psql $DATABASE_URL -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';")

if [ "$TABLE_COUNT" = "0" ]; then
    echo "Database is empty. Running init.sql..."
    psql $DATABASE_URL -f /app/init.sql
else
    echo "Database is already initialized. Skipping init.sql."
fi

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
