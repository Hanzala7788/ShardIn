#!/bin/bash

# Quick fix for entrypoint.sh permission issue
# Run this on your EC2 instance

echo "Fixing entrypoint.sh permissions..."

cd ~/ShardIn

# Fix permissions
chmod +x entrypoint.sh

# Stop containers
docker compose down

# Rebuild and start
docker compose up -d --build

# Wait for services
sleep 10

# Run migrations
docker compose exec web python manage.py migrate --noinput

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Show status
docker compose ps

echo ""
echo "✅ Fix applied! Check the status above."
