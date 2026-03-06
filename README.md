# School Management - Gestion Scolaire SaaS

Une application Django complète pour la gestion scolaire prête pour la production.

## 🚀 Installation Rapide

### 1. Prérequis
- Python 3.10+
- pip
- virtualenv ou venv

### 2. Créer un environnement virtuel

```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration initiale

```bash
# Copier le fichier .env
Copy-Item .env.example .env  # Windows
cp .env.example .env          # Linux/Mac

# Générer une nouvelle SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copier la clé et la mettre dans .env
```

### 5. Initialiser la base de données

```bash
# Créer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Charger les données initiales (optionnel)
# python manage.py loaddata fixtures/initial_data.json
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

Accédez à : http://localhost:8000/admin

## 📦 Structure du projet

```
school_management/
├── school_management/          # Configuration principale
│   ├── settings.py            # Configuration Django
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # WSGI pour production
│   ├── asgi.py                # ASGI pour WebSockets
│   ├── celery.py              # Configuration Celery
│   └── __init__.py
├── apps/                       # Applications Django
│   ├── users/                 # Gestion des utilisateurs
│   ├── schools/               # Gestion des écoles
│   ├── students/              # Gestion des étudiants
│   ├── teachers/              # Gestion des enseignants
│   ├── courses/               # Gestion des cours
│   └── grades/                # Gestion des notes
├── templates/                  # Templates HTML
├── static/                     # Fichiers statiques (CSS, JS)
├── media/                      # Fichiers uploadés
├── logs/                       # Fichiers journaux
├── manage.py                   # Gestion Django
├── requirements.txt            # Dépendances Python
├── .env.example                # Exemple de configuration
└── README.md                   # Ce fichier
```

## ⚙️ Configuration

### Développement (SQLite)

Le fichier `.env` est préconfigié pour le développement avec SQLite :

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (PostgreSQL)

Pour passer en production, modifiez le `.env` :

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Décommenter et configurer PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=school_management_db
DB_USER=postgres
DB_PASSWORD=your-strong-password
DB_HOST=your-database-host.com
DB_PORT=5432
```

### Installation des dépendances en production

```bash
pip install -r requirements.txt
pip install psycopg2-binary  # Pour PostgreSQL
pip install gunicorn         # Serveur WSGI
```

## 🗄️ Base de données

### Migrations

```bash
# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Afficher l'état des migrations
python manage.py showmigrations
```

### Sauvegarde et restauration

```bash
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json
```

## 🔐 Sécurité

### Bonnes pratiques implémentées

✅ **settings.py optimisé pour production**
- SSL/HTTPS obligatoire en production
- CSRF protection activée
- XSS protection
- HSTS (HTTP Strict Transport Security)
- Content Security Policy

✅ **Authentification**
- Session-based par défaut
- Tokens disponibles avec Django REST Framework
- Password validation robuste

✅ **Variables sensibles**
- Utilisation de `.env` pour les secrets
- `SECRET_KEY` externe
- Pas de secrets en dur dans le code

### Générer une nouvelle SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📚 Commands utiles

```bash
# Créer une nouvelle application
python manage.py startapp app_name

# Créer un superutilisateur
python manage.py createsuperuser

# Nettoyage de la base de données
python manage.py flush

# Shell Django interactif
python manage.py shell

# Vérifier la configuration
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Générer les fichiers de traduction
python manage.py makemessages -l fr

# Compiler les traductions
python manage.py compilemessages
```

## 🚀 Déploiement

### Avec Gunicorn

```bash
# Installer gunicorn
pip install gunicorn

# Lancer l'application
gunicorn school_management.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Avec Docker (optionnel)

Créez un fichier `Dockerfile` :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "school_management.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Avec Nginx

Configuration basique Nginx :

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 API REST Framework

L'application utilise Django REST Framework pour l'API :

### Endpoints d'authentification
- `POST /api-auth/login/` - Se connecter
- `POST /api-auth/logout/` - Se déconnecter

### Pagination
Configuration par défaut : 20 résultats par page

### Throttling
- Utilisateurs authentifiés : 1000 requêtes/heure
- Utilisateurs anonymes : 100 requêtes/heure

## 📧 Configuration Email

### Pour Gmail (SMTP)
1. Activez "Accès aux applications moins sécurisées"
2. Utilisez une "Mot de passe d'application"
3. Configurez dans `.env` :

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application
```

### Console Email (développement)
Par défaut, les emails sont affichés dans la console.

## 🔄 Celery (Tâches asynchrones)

Configuration pour les tâches en arrière-plan :

```bash
# Lancer le worker Celery
celery -A school_management worker -l info

# Lancer Celery Beat (planificateur)
celery -A school_management beat -l info
```

## 🧪 Tests

```bash
# Lancer les tests
python manage.py test

# Avec couverture de code
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Logging

Les logs sont enregistrés dans `logs/django.log` avec rotation automatique (max 15MB par fichier).

## 🌐 Internationalisation (i18n)

```bash
# Créer les fichiers de traduction
python manage.py makemessages -l fr

# Compiler les traductions
python manage.py compilemessages
```

## 📖 Ressources

- [Documentation Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [django-environ](https://django-environ.readthedocs.io/)
- [Celery](https://docs.celeryproject.org/)

## 🔗 Dépôt GitHub

URL du dépôt : [https://github.com/kilongodimer-cmyk/school-management](https://github.com/kilongodimer-cmyk/school-management)

## 📄 Licence

MIT

## 👨‍💻 Support

Pour l'aide et le support, créez une issue dans le repository : https://github.com/kilongodimer-cmyk/school-management/issues

---

**Projet prêt pour evoluer vers la production avec PostgreSQL, Redis et déploiement sur serveurs cloud (Heroku, AWS, DigitalOcean, etc.)**
