#!/usr/bin/env python
"""
Script to run migrations for the academics app with proper sys.path setup.
"""
import sys
import os

# Add the project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

# Setup Django
import django
django.setup()

# Import management commands
from django.core.management import execute_from_command_line

# Run migrations for academics app
if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'migrate', 'academics'])
