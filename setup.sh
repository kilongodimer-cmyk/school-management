#!/bin/bash

# Script d'installation et configuration du projet Django
# School Management - Gestion Scolaire SaaS

echo ""
echo "============================================"
echo "School Management - Gestion Scolaire SaaS"
echo "============================================"
echo ""

# 1. Créer l'environnement virtuel
echo "[1/6] Création de l'environnement virtuel..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible de créer l'environnement virtuel"
    exit 1
fi
echo "✓ Environnement virtuel créé"

# 2. Activer l'environnement virtuel
echo ""
echo "[2/6] Activation de l'environnement virtuel..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'activer l'environnement virtuel"
    exit 1
fi
echo "✓ Environnement virtuel activé"

# 3. Installer les dépendances
echo ""
echo "[3/6] Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'installer les dépendances"
    exit 1
fi
echo "✓ Dépendances installées"

# 4. Copier le fichier .env
echo ""
echo "[4/6] Configuration de l'environnement..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Fichier .env créé"
    echo "⚠  Veuillez éditer le fichier .env et mettre à jour la SECRET_KEY"
else
    echo "ⓘ Fichier .env existe déjà"
fi

# 5. Créer les migrations
echo ""
echo "[5/6] Création de la base de données..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible de créer les migrations"
    exit 1
fi
echo "✓ Migrations appliquées"

# 6. Créer un superutilisateur
echo ""
echo "[6/6] Création du superutilisateur..."
echo "Entrez les informations pour l'administrateur:"
python manage.py createsuperuser
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible de créer le superutilisateur"
    exit 1
fi
echo "✓ Superutilisateur créé"

echo ""
echo "============================================"
echo "✓ Installation terminée avec succès!"
echo "============================================"
echo ""
echo "Prochaines étapes:"
echo ""
echo "1. Optionnel: Générer une nouvelle SECRET_KEY:"
echo "   python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo ""
echo "2. Mettre à jour le fichier .env avec cette clé:"
echo "   SECRET_KEY=votre-clé"
echo ""
echo "3. Lancer le serveur de développement:"
echo "   python manage.py runserver"
echo ""
echo "4. Accéder à l'admin Django:"
echo "   http://localhost:8000/admin"
echo ""
