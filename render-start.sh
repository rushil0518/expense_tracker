#!/usr/bin/env bash
export PYTHONUNBUFFERED=1

# Run migrations (optional if not using Django DB)
# python manage.py migrate

# Run collectstatic
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:$PORT

git add .
git commit -m "Add Render start script"
