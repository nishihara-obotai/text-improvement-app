#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Install gunicorn for production
pip install gunicorn

# Collect static files
python project/manage.py collectstatic --no-input

# Run migrations
python project/manage.py migrate

# Create users for production
python scripts/create_users.py

