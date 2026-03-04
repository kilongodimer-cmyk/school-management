# COMMANDES ESSENTIELLES - QUICK START

## 🚀 DÉMARRAGE RAPIDE

### Windows
```powershell
# 1. Installation automatique
.\setup.bat

# OU installation manuelle
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Linux / Mac
```bash
# 1. Installation automatique
chmod +x setup.sh
./setup.sh

# OU installation manuelle
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Accès** : http://localhost:8000/admin

---

## 📁 STRUCTURE INITIALE

```
school_management/
├── school_management/       # Configuration Django
├── manage.py               # Commandes Django
├── requirements.txt        # Dépendances
├── .env.example           # Variables d'env
├── README.md              # Documentation
└── INSTALL.md             # Guide complet
```

---

## 🛠️ COMMANDES COURANTES

### Gestion de la base de données
```bash
# Créer une migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir l'état des migrations
python manage.py showmigrations

# Rollback
python manage.py migrate app_name 0001
```

### Utilisateurs & Sécurité
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Changer le mot de passe d'un utilisateur
python manage.py changepassword username

# Nettoyer les sessions expirées
python manage.py clearsessions
```

### Gestion des données
```bash
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json

# Réinitialiser la BD (ATTENTION: perte de données)
python manage.py flush
```

### Applications
```bash
# Créer une nouvelle app
python manage.py startapp app_name

# Vérifier la configuration
python manage.py check

# Shell interactif
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```

### Développement
```bash
# Serveur de développement
python manage.py runserver
python manage.py runserver 0.0.0.0:8001  # Port personnalisé

# Lancer les tests
python manage.py test

# Avec couverture
coverage run --source='.' manage.py test
coverage report
```

---

## 🗄️ CONFIGURATION BASE DE DONNÉES

### SQLite (Développement - par défaut)
Aucune configuration supplémentaire, utilise `db.sqlite3`

### PostgreSQL (Production)

#### 1. Installer PostgreSQL
```bash
# Windows (Chocolatey)
choco install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS (Homebrew)
brew install postgresql
```

#### 2. Créer la base de données
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Commandes SQL
CREATE DATABASE school_management_db;
CREATE USER school_mgmt_user WITH PASSWORD 'secure_password';
ALTER ROLE school_mgmt_user SET client_encoding TO 'utf8';
ALTER ROLE school_mgmt_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE school_management_db TO school_mgmt_user;
\q
```

#### 3. Configurer .env
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=school_management_db
DB_USER=school_mgmt_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

#### 4. Installer le driver
```bash
pip install psycopg2-binary
```

#### 5. Appliquer les migrations
```bash
python manage.py migrate
```

---

## 🐳 DOCKER

### Démarrer
```bash
# Lancer tous les services
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f web
```

### Commandes utiles
```bash
# Migrations
docker-compose exec web python manage.py migrate

# Superutilisateur
docker-compose exec web python manage.py createsuperuser

# Shell Django
docker-compose exec web python manage.py shell

# Arrêter
docker-compose down

# Nettoyer tout
docker-compose down -v
```

---

## 📱 API REST

### Endpoints disponibles
```
GET    /api/v1/profiles/              # Liste des profils
POST   /api/v1/profiles/              # Créer un profil
GET    /api/v1/profiles/{id}/         # Détail d'un profil
PUT    /api/v1/profiles/{id}/         # Modifier un profil
DELETE /api/v1/profiles/{id}/         # Supprimer un profil
GET    /api/v1/profiles/me/           # Mon profil
PUT    /api/v1/profiles/update_me/    # Mettre à jour mon profil
```

### Authentification
```bash
# Les endpoints API nécessitent une authentification
# Session-based ou Token (à configurer)

# Header pour les requêtes
Authorization: Token your-token-here
```

---

## 🔐 SÉCURITÉ

### Générer une nouvelle SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Variables sensibles dans .env
```env
DEBUG=False  # Toujours False en production
SECRET_KEY=votre-clé-sécurisée
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Checklist sécurité
- [ ] SECRET_KEY unique et complexe
- [ ] DEBUG = False en production
- [ ] ALLOWED_HOSTS configuré
- [ ] HTTPS/SSL activé
- [ ] Database password robuste
- [ ] .env non commité
- [ ] Logs en fichier
- [ ] Sauvegardes automatiques

---

## 📧 EMAIL

### Configuration Gmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Tester l'envoi d'email
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test',
    'Message de test',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

---

## 🔄 CELERY (Tâches asynchrones)

### Installer Redis
```bash
# Windows (Chocolatey)
choco install redis

# Linux (APT)
sudo apt-get install redis-server

# macOS (Homebrew)
brew install redis
```

### Lancer les workers
```bash
# Worker Celery
celery -A school_management worker -l info

# Beat Scheduler
celery -A school_management beat -l info
```

### Créer une tâche
```python
# tasks.py
from celery import shared_task

@shared_task
def send_email_task(email):
    # Tâche longue
    pass

# views.py
from .tasks import send_email_task
send_email_task.delay(user_email)
```

---

## 📊 MONITORING

### Logs
```bash
# Voir les logs Django
tail -f logs/django.log

# Windows
Get-Content logs/django.log -Tail 100 -Wait
```

### Performances
```bash
# Shell Django
python manage.py shell
from django.db import connection
connection.queries  # Affiche les requêtes SQL
```

### Fichiers statiques
```bash
# Collecter les statics
python manage.py collectstatic --noinput --clear

# Servir les statics en production
# Utiliser Nginx ou CDN
```

---

## 🚀 DÉPLOIEMENT

### Production checklist
- [ ] Installer PostgreSQL
- [ ] Créer la base de données
- [ ] Générer une nouvelle SECRET_KEY
- [ ] Installer Gunicorn
- [ ] Configurer Nginx
- [ ] Mettre en place SSL
- [ ] Installer Redis
- [ ] Configurer Celery
- [ ] Mettre en place les logs
- [ ] Configurer les backups

### Lancer en production
```bash
# Avec Gunicorn
gunicorn school_management.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Avec Systemd (Linux)
sudo systemctl start school-management
sudo systemctl enable school-management
```

---

## ❌ DÉPANNAGE

### Import error
```bash
# Assurez-vous que l'env virtuel est activé
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Réinstallez les paquets
pip install -r requirements.txt
```

### No such table
```bash
python manage.py migrate
```

### Port déjà utilisé
```bash
python manage.py runserver 8001
```

### Erreur PostgreSQL
```bash
# Vérifier que PostgreSQL est lancé
pg_isready -h localhost -p 5432

# Redémarrer PostgreSQL
sudo service postgresql restart  # Linux
```

### Permission denied
```bash
chmod +x manage.py  # Linux/Mac
chmod 755 -R media/
```

---

## 📚 RESSOURCES

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Celery](https://docs.celeryproject.org/)
- [Docker](https://docs.docker.com/)
- [Nginx](https://nginx.org/en/docs/)

---

## 💡 PROCHAINES ÉTAPES

1. Exécuter `setup.bat` ou `setup.sh`
2. Créer les applications (`python manage.py startapp app_name`)
3. Définir les modèles
4. Créer les migrations
5. Configurer l'admin Django
6. Créer les API REST
7. Mettre en place l'authentification
8. Ajouter les tâches Celery
9. Tester localement
10. Déployer en production

**Bon développement ! 🎉**
