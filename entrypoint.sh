#!/bin/sh

# Wait for the MySQL database to be ready
/code/wait-for-it.sh db:3306 --timeout=60 --strict -- echo "MySQL is up"

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec "$@"
