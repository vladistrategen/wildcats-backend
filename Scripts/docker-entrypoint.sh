#!/bin/bash
set -e
echo "Starting entrypoint.sh"
# Wait for MySQL to be ready
./wait-for-it.sh db:3306 --timeout=30

#django health check
python manage.py check_health

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000