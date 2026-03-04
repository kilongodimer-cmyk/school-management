# Commands de déploiement et scripts utiles

## Commandes d'installation complètes

### 1. Déploiement Initial (Développement)
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. Transition vers Production (PostgreSQL)

#### Sur le serveur
```bash
# 1. Créer la base de données PostgreSQL
createdb school_management_db
createuser school_mgmt_user
psql -c "ALTER USER school_mgmt_user PASSWORD 'secure_password';"
psql -c "ALTER ROLE school_mgmt_user SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE school_mgmt_user SET default_transaction_isolation TO 'read committed';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE school_management_db TO school_mgmt_user;"

# 2. Configurer les variables d'environnement
export DEBUG=False
export SECRET_KEY="votre-clé-secrète-sécurisée"
export DB_ENGINE=django.db.backends.postgresql
export DB_NAME=school_management_db
export DB_USER=school_mgmt_user
export DB_PASSWORD=secure_password
export DB_HOST=localhost
export DB_PORT=5432

# 3. Installer les dépendances
pip install -r requirements.txt
pip install psycopg2-binary
pip install gunicorn

# 4. Créer les migrations
python manage.py migrate

# 5. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Lancer avec Gunicorn
gunicorn school_management.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
```

### 3. Avec Systemd (Linux)

Créer `/etc/systemd/system/school-management.service` :

```ini
[Unit]
Description=School Management Django Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/school_management
Environment="PATH=/var/www/school_management/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=school_management.settings"
EnvironmentFile=/var/www/school_management/.env
ExecStart=/var/www/school_management/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/school-management.sock \
    school_management.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activation :
```bash
sudo systemctl daemon-reload
sudo systemctl enable school-management
sudo systemctl start school-management
sudo systemctl status school-management
```

### 4. Avec Docker

Créer `Dockerfile` à la racine :

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Collecte des statics
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "school_management.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Créer `docker-compose.yml` :

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: school_management_db
      POSTGRES_USER: school_mgmt_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             gunicorn school_management.wsgi:application --bind 0.0.0.0:8000 --workers 4"
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

Lancer :
```bash
docker-compose up -d
```

## Commandes de maintenance

### Sauvegarde
```bash
# Sauvegarde de la base de données
python manage.py dumpdata > backup.json

# Avec date
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# PostgreSQL uniquement
pg_dump -U school_mgmt_user school_management_db > backup_pg.sql
```

### Restauration
```bash
# Restaurer depuis JSON
python manage.py loaddata backup.json

# PostgreSQL uniquement
psql -U school_mgmt_user school_management_db < backup_pg.sql
```

### Nettoyage
```bash
# Supprimer les sessions expirées
python manage.py clearsessions

# Nettoyer les fichiers temporaires
python manage.py shell -c "from django.core.files.storage import default_storage; import os; [os.remove(f) for f in os.listdir('media/temp/') if os.path.isfile(f)]"
```

### Monitoring
```bash
# Vérifier la configuration
python manage.py check

# Vérifier les migrations non appliquées
python manage.py showmigrations

# Vérifier les performances des requêtes
python manage.py shell
# Puis dans le shell :
# from django.db import connection
# from django.test.utils import override_settings
# connection.queries  # Affiche toutes les requêtes SQL
```

## Dépannage

### Erreur de migration
```bash
# Afficher les migrations
python manage.py showmigrations

# Rollback d'une migration
python manage.py migrate app_name 0001

# Créer une nouvelle migration vide
python manage.py makemigrations --empty app_name --name migration_name
```

### Problèmes de permissions
```bash
# Linux/Mac - Donner les permissions
chmod +x manage.py
chmod 755 -R media/
chmod 755 -R staticfiles/
```

### Erreurs de base de données
```bash
# Réinitialiser la base de données
python manage.py flush

# Recréer les migrations
python manage.py makemigrations
python manage.py migrate
```

## Scaling en production

### Load Balancing avec Nginx + Gunicorn
```nginx
upstream django_app {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name schoolmanagement.com www.schoolmanagement.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/school_management/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/school_management/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_read_timeout 120s;
    }
}
```

### Cache Redis
```python
# Utiliser le cache dans les views
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 5)  # Cache 5 minutes
def my_view(request):
    pass

# Ou manuellement
cache.set('my_key', 'my_value', 3600)
value = cache.get('my_key')
```

### Celery pour les tâches lourdes
```python
# tasks.py
from celery import shared_task

@shared_task
def generate_report():
    # Tâche longue
    pass

# views.py
from .tasks import generate_report

def trigger_report(request):
    generate_report.delay()
    return JsonResponse({'status': 'Report generation started'})
```

## Monitoring et Logging

### Logs dans AWS CloudWatch
```python
# settings.py
LOGGING = {
    ...
    'handlers': {
        'cloudwatch': {
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group': 'school-management',
            'stream_name': 'app',
        },
    },
}
```

### Sentry pour les erreurs
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

---

**Votre application est maintenant complète et prête pour tous les environnements (dev, staging, production) !**
