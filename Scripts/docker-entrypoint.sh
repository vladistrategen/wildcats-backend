#!/bin/bash

echo "Starting entrypoint.sh"

set -e
# Wait for MySQL to be ready
/app/Scripts/wait-for-it.sh db:3306 --timeout=30

python manage.py makemigrations
# Apply migrations
python manage.py migrate

python /app/Scripts/populate_db.py

#django health check
python manage.py check_health


# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000