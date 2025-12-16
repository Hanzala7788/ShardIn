#!/bin/sh

echo "Waiting for Postgres..."

# Wait until Postgres is ready
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Postgres started"

# Run migrations
python manage.py migrate --noinput

# Collect static files (even if you're not using them, Django expects this)
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

# Start Gunicorn with 4 workers, bound to 0.0.0.0:8000
exec gunicorn config.wsgi:application \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --log-level info \
    --access-logfile -
