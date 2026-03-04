@echo off
REM Script pour initialiser l'app accounts
REM Crée les migrations, les applique et configure les données initiales

echo.
echo ============================================
echo Initialisation de l'app accounts
echo ============================================
echo.

REM Vérifier l'environnement virtuel
if not exist "venv\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouvé
    echo Veuillez d'abord exécuter setup.bat
    pause
    exit /b 1
)

REM Activer l'environnement
call venv\Scripts\activate.bat

REM 1. Créer les migrations
echo [1/4] Création des migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERREUR: Echec de la création des migrations
    pause
    exit /b 1
)
echo ✓ Migrations créées

REM 2. Appliquer les migrations
echo.
echo [2/4] Application des migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERREUR: Echec de l'application des migrations
    pause
    exit /b 1
)
echo ✓ Migrations appliquées

REM 3. Créer un superutilisateur
echo.
echo [3/4] Création du superutilisateur...
echo Entrez les informations du superutilisateur:
python manage.py createsuperuser
if errorlevel 1 (
    echo ERREUR: Echec de la création du superutilisateur
    pause
    exit /b 1
)
echo ✓ Superutilisateur créé

REM 4. Créer une école test
echo.
echo [4/4] Création d'une école test avec utilisateurs...
python manage.py create_school_with_users --name "École de Test" --code "ET001" --email "test@ecole.com" --director "Pierre Directeur"
if errorlevel 1 (
    echo ERREUR: Echec de la création de l'école
    pause
    exit /b 1
)
echo ✓ École test créée

echo.
echo ============================================
echo ✓ Initialisation terminée!
echo ============================================
echo.
echo Commandes utiles:
echo.
echo 1. Lancer le serveur:
echo    python manage.py runserver
echo.
echo 2. Accéder à l'admin:
echo    http://localhost:8000/admin
echo.
echo 3. Créer une autre école:
echo    python manage.py create_school_with_users --name "Ma École" --code "ME001"
echo.
echo 4. Exécuter les tests:
echo    python manage.py test apps.accounts
echo.
pause
