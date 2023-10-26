#!/bin/bash
set -e

# Wait for MySQL to be ready
./wait-for-it.sh db:3306 --timeout=30

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
python manage.py runserver 0.0.0.0:8000