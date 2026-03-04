import os, sys
sys.path.insert(0, r"C:\Users\Dell\school_management")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_management.settings_production")
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = "merdikilongo"
email = "kilongodimer@example.com"
password = "Dimer@07"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser créé")
else:
    print("Superuser existe déjà")