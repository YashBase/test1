#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python myfilemanager/manage.py migrate

# Collect static files
python myfilemanager/manage.py collectstatic --noinput

# Start the Gunicorn server
gunicorn myfilemanager.wsgi
