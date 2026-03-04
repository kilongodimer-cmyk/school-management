# Déploiement sur Render — Guide rapide

Ce guide explique comment déployer la version production du projet Django SaaS `school_management` sur Render, configurer la base PostgreSQL et automatiser les migrations via GitHub Actions.

1) Pré-requis
- Avoir un dépôt Git (branche `main` utilisée pour déploiement)
- Compte Render
- Compte GitHub (pour Actions)

2) Fichiers importants ajoutés
- `school_management/settings_production.py` — configuration production, lecture de `.env` et WhiteNoise
- `Procfile` — commande de démarrage Gunicorn
- `render.yaml` — manifeste Render (build/start + variables placeholders)
- `.env.example` — exemple des variables d'environnement à renseigner
- `.github/workflows/ci.yml` — workflow CI : tests → migrate (remote DB) → trigger Render deploy

3) Créer la base PostgreSQL sur Render
 - Dans le dashboard Render → New → PostgreSQL → créer une base (choisir plan)
 - Copier la `DATABASE_URL` fournie

4) Variables d'environnement (Render service)
 - Dans votre service web Render, Settings → Environment → Environment Variables, ajouter :
   - `SECRET_KEY` — clé secrète longue (ne pas partager)
   - `DATABASE_URL` — fournie par la base PostgreSQL
   - `ALLOWED_HOSTS` — e.g. yourdomain.com
   - `CSRF_TRUSTED_ORIGINS` — e.g. https://yourdomain.com
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
   - `SECURE_SSL_REDIRECT=1`

5) Configurer GitHub Secrets (pour CI)
 - `DATABASE_URL` (valeur de production)
 - `SECRET_KEY`
 - `RENDER_API_KEY` (voir Render → Account → API Keys)
 - `RENDER_SERVICE_ID` (ID du service à retrouver dans l'URL du service ou via API)

6) Déployer
 - Pousser sur `main` : Render déclenchera un build automatique.
 - Le workflow GitHub Actions `CI and Render deploy` lancera :
   1. Tests (optionnel)
   2. `python manage.py migrate` sur la `DATABASE_URL` (exécuté depuis GitHub Actions)
   3. Déclenche un build sur Render via API (collectstatic s'exécute pendant le build sur Render si configuré)

7) Commandes utiles (PowerShell)
```
pip install -r requirements.txt
# copier .env.example -> .env et remplir
Copy-Item .env.example .env
$env:DJANGO_SETTINGS_MODULE="school_management.settings_production"
$env:SECRET_KEY="votre-cle-secrete-local"
$env:DATABASE_URL="sqlite:///db.sqlite3"
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

8) Checklist post-déploiement
- `DEBUG=False` confirmé
- `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` configurés
- Isolation multi-écoles testée (tenant middleware / filtre sur modèles)
- Génération PDF testée (`reportlab`)
- CRUD élèves, notes, paiements testés
- Login/logout et dashboard fonctionnels
- Fichiers statiques servis (`/static/`), médias (`/media/`)

Si vous voulez, je peux :
- (1) Ajouter un `postdeploy` automatique pour exécuter `migrate` et `collectstatic` directement sur Render (si vous préférez exécuter les commandes côté hébergeur), ou
- (2) Ajouter des vérifications automatisées (healthchecks, Sentry).
