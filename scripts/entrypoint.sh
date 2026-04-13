#!/bin/bash

echo "Waiting for Redis..."

while ! nc -z redis 6379; do
    sleep 2
done

echo "Redis is ready"

echo "Running migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Compiling translations..."
python3 manage.py compilemessages || true

if [ "$BLOG_SEED_DATA" = "true" ]; then
    echo "Seeding datebase..."
    python3 manage.py seed
fi

echo "Starting app."

exec "$@"