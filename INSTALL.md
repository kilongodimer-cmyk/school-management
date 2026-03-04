# INSTALLATION ET CONFIGURATION COMPLÈTES

## 📋 Vue d'ensemble

Ce projet Django **School Management** est une application SaaS pour la gestion scolaire, complètement configurée pour :
- ✅ Développement avec SQLite
- ✅ Production avec PostgreSQL
- ✅ Déploiement Docker
- ✅ Celery pour les tâches asynchrones
- ✅ Redis pour le caching
- ✅ Sécurité production-ready

---

## 🔧 COMMANDES D'INSTALLATION

### Option 1 : Installation automatique (Windows)

```powershell
# Double-cliquez sur setup.bat ou exécutez:
.\setup.bat
```

### Option 2 : Installation automatique (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

### Option 3 : Installation manuelle (Tous les systèmes)

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement (Windows)
.\venv\Scripts\activate
# Ou (Linux/Mac)
source venv/bin/activate

# 3. Mettre à jour pip
pip install --upgrade pip

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Copier et configurer .env
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# 6. Générer une SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 7. Mettre à jour .env avec la clé
# Éditez .env et remplacez la SECRET_KEY

# 8. Créer la base de données
python manage.py migrate

# 9. Créer un superutilisateur
python manage.py createsuperuser

# 10. Lancer le serveur
python manage.py runserver
```

---

## 🎯 CRÉER DES APPLICATIONS DJANGO

Voici comment créer une nouvelle application (ex: users, schools, students) :

```bash
# Créer l'app
python manage.py startapp apps.users

# Ou créer plusieurs apps:
python manage.py startapp apps.schools
python manage.py startapp apps.students
python manage.py startapp apps.teachers
python manage.py startapp apps.courses
python manage.py startapp apps.grades
```

### Ajouter l'app à settings.py

```python
INSTALLED_APPS = [
    # ...
    'apps.users',
    'apps.schools',
    'apps.students',
    'apps.teachers',
    'apps.courses',
    'apps.grades',
]
```

### Exemple de modèle (apps/users/models.py)

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    school = models.ForeignKey('schools.School', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
```

---

## 🗄️ CONFIGURATION BASE DE DONNÉES

### Développement - SQLite (par défaut)

Le fichier `.env.example` est préconfiguré pour SQLite :

```env
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
# La base de données SQLite sera créée automatiquement dans `db.sqlite3`
```

### Production - PostgreSQL

#### Installation PostgreSQL

**Windows (avec Chocolatey) :**
```powershell
choco install postgresql
```

**Ubuntu/Debian :**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**Mac (avec Homebrew) :**
```bash
brew install postgresql
brew services start postgresql
```

#### Créer la base de données

```bash
# Accéder à psql
psql -U postgres

# Commandes SQL
CREATE DATABASE school_management_db;
CREATE USER school_mgmt_user WITH PASSWORD 'your_secure_password';
ALTER ROLE school_mgmt_user SET client_encoding TO 'utf8';
ALTER ROLE school_mgmt_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE school_mgmt_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE school_management_db TO school_mgmt_user;
\q  # Quitter
```

#### Configurer le .env

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=school_management_db
DB_USER=school_mgmt_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Installer le driver PostgreSQL

```bash
pip install psycopg2-binary
```

#### Appliquer les migrations

```bash
python manage.py migrate
```

---

## ⚙️ CONFIGURATION SETTINGS.PY - BONNES PRATIQUES

### ✅ Structuration recommandée

Votre `settings.py` principale contient :

1. **Variables d'environnement** - Utilise `django-environ`
2. **Configuration de base** - SECRET_KEY, DEBUG, ALLOWED_HOSTS
3. **Apps et Middleware** - Configuration Django
4. **Base de données** - Flexible SQLite/PostgreSQL
5. **Authentification** - Sécurité renforcée
6. **REST Framework** - API configuration
7. **Cache** - LocMemCache (dev) ou Redis (prod)
8. **Logging** - Rotation des logs avec 15MB max
9. **Email** - Configuration SMTP
10. **Celery** - Tâches asynchrones
11. **Sécurité production** - SSL, HSTS, CSP, etc.

### 📁 Settings par environnement

**Développement (settings_dev.py) :**
```python
from .settings import *

INSTALLED_APPS += ['django_extensions']
LOGGING['loggers']['django']['level'] = 'DEBUG'
```

**Production (settings_prod.py) :**
```python
from .settings import *

DEBUG = False
SECRET_KEY = env('SECRET_KEY')  # OBLIGATOIRE
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
# ... autres configurations de sécurité
```

### 🚀 Utiliser une configuration spécifique

```bash
# Développement
python manage.py runserver --settings=school_management.settings_dev

# Production
python manage.py migrate --settings=school_management.settings_prod
```

---

## 🔐 SÉCURITÉ - CONFIGURATION PRODUCTION

### 1. Générer une nouvelle SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Configuration de sécurité (automatique en production)

```python
# Dans settings.py (activé quand DEBUG=False)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
```

### 3. Certificat SSL

**Avec Let's Encrypt (gratuit) :**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 4. Variables sensibles

Ne jamais commit `.env` :
```bash
# .gitignore
.env
.env.local
*.sqlite3
```

---

## 🐳 DOCKER - DÉPLOIEMENT

### Démarrer avec Docker Compose

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Lancer le projet
docker-compose up -d

# Vérifier les services
docker-compose ps

# Voir les logs
docker-compose logs web

# Arrêter
docker-compose down
```

### Services disponibles

- **web** : Application Django (port 8000)
- **db** : PostgreSQL (port 5432)
- **redis** : Cache Redis (port 6379)
- **celery** : Worker asynchrone
- **celery-beat** : Tâches planifiées

### Exécuter des commandes

```bash
# Migrations
docker-compose exec web python manage.py migrate

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Shell Django
docker-compose exec web python manage.py shell

# Collecte des statics
docker-compose exec web python manage.py collectstatic
```

---

## 📊 GESTION DE DONNÉES

### Migrations

```bash
# Créer une migration
python manage.py makemigrations app_name

# Voir les migrations
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate

# Rollback d'une migration
python manage.py migrate app_name 0001

# Faire une migration vide (pour du SQL personnalisé)
python manage.py makemigrations --empty app_name --name migration_name
```

### Sauvegarde/Restauration

```bash
# Exporter les données
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Importer les données
python manage.py loaddata backup.json

# PostgreSQL uniquement
pg_dump -U school_mgmt_user school_management_db > backup.sql
psql -U school_mgmt_user school_management_db < backup.sql
```

### Nettoyage

```bash
# Supprimer les sessions expirées
python manage.py clearsessions

# Réinitialiser la base (ATTENTION: perte de données)
python manage.py flush
```

---

## 🎮 COMMANDES UTILES

```bash
# Vérifier la configuration
python manage.py check

# Shell interactif Django
python manage.py shell

# Créer un superutilisateur supplémentaire
python manage.py createsuperuser

# Charger des données initiales
python manage.py loaddata fixtures/initial_data.json

# Générer les traductions
python manage.py makemessages -l fr

# Compiler les traductions
python manage.py compilemessages

# Collecter les fichiers statiques
python manage.py collectstatic

# Tests
python manage.py test

# Exécuter les tâches Celery
celery -A school_management worker -l info

# Planificateur Celery
celery -A school_management beat -l info
```

---

## 📈 ÉVOLUTION DU PROJET

### Phase 1 : Développement ✅ (Actuellement)
- SQLite
- Django admin
- API REST basique
- Redis local

### Phase 2 : Staging
- PostgreSQL
- Nginx
- Gunicorn (4 workers)
- Redis distant
- Certificat SSL

### Phase 3 : Production
- Load balancer
- Multi-workers Gunicorn
- CDN pour les statics
- Monitoring (Sentry, NewRelic)
- Backups automatiques
- Scaling horizontal

---

## 🆘 DÉPANNAGE

### Erreur : ModuleNotFoundError

```bash
# Assurez-vous que l'environnement virtuel est activé
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Réinstallez les dépendances
pip install -r requirements.txt
```

### Erreur : No such table

```bash
# Appliquez les migrations
python manage.py migrate
```

### Erreur : Permission denied

```bash
# Linux/Mac
chmod +x manage.py
chmod 755 -R media/
```

### Database connection refused

```bash
# Vérifiez que PostgreSQL est lancé
# Windows
net start postgresql-x64-15
# Linux/Mac
brew services start postgresql
# ou
sudo service postgresql start
```

### Redis connection refused

```bash
# Installez Redis
# Windows (avec Chocolatey)
choco install redis

# Linux/Mac
brew install redis
redis-server
```

---

## 📚 STRUCTURE FINALE DU PROJET

```
school_management/
├── school_management/               # Configuration principale
│   ├── __init__.py                 # Celery init
│   ├── settings.py                 # Configuration principale
│   ├── settings_dev.py             # Config développement
│   ├── settings_prod.py            # Config production
│   ├── urls.py                     # Routes principales
│   ├── wsgi.py                     # WSGI production
│   ├── asgi.py                     # ASGI WebSockets
│   └── celery.py                   # Configuration Celery
├── apps/                           # Applications Django
│   ├── __init__.py
│   ├── users/                      # Gestion utilisateurs
│   ├── schools/                    # Gestion écoles
│   ├── students/                   # Gestion étudiants
│   ├── teachers/                   # Gestion enseignants
│   ├── courses/                    # Gestion cours
│   └── grades/                     # Gestion notes
├── templates/                      # Templates HTML
├── static/                         # CSS, JS, images
├── media/                          # Fichiers uploadés
├── logs/                           # Logs application
├── manage.py                       # Gestion Django
├── requirements.txt                # Dépendances Python
├── .env.example                    # Template .env
├── .gitignore                      # Fichiers à ignorer
├── README.md                       # Documentation
├── DEPLOYMENT.md                   # Guide déploiement
├── INSTALL.md                      # Ce fichier
├── Dockerfile                      # Conteneurisation
├── docker-compose.yml              # Services Docker
├── nginx.conf                      # Configuration Nginx
├── school-management.service       # Service Systemd
├── setup.sh                        # Installation Linux/Mac
└── setup.bat                       # Installation Windows
```

---

## ✨ PROCHAINES ÉTAPES

1. ✅ Installer le projet (setup.bat ou setup.sh)
2. ✅ Créer les applications (users, schools, etc.)
3. ✅ Définir les modèles
4. ✅ Créer les migrations (`python manage.py makemigrations`)
5. ✅ Appliquer les migrations (`python manage.py migrate`)
6. ✅ Créer les API avec Django REST Framework
7. ✅ Configurer l'authentification
8. ✅ Mettre en place les tâches Celery
9. ✅ Tester et déboguer
10. ✅ Déployer en production

---

**Votre projet Django SaaS est maintenant entièrement configuré et prêt ! 🚀**
