#!/usr/bin/env bash
set -euo pipefail

echo "Running Render post-deploy tasks: migrate and collectstatic"

# Ensure DJANGO_SETTINGS_MODULE is set (should be set via Render env)
: ${DJANGO_SETTINGS_MODULE:?"DJANGO_SETTINGS_MODULE must be set in environment"}

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Post-deploy tasks completed"
