# Documentation de l'App Accounts

## Vue d'ensemble

L'app `accounts` gère la gestion complète des utilisateurs et des écoles dans le système SaaS de gestion scolaire.

## Modèles

### 1. School (École)

Représente une école dans le système SaaS.

**Champs principaux:**
- `name` : Nom unique de l'école
- `code` : Code unique pour identifier l'école
- `email` : Email de l'école (unique)
- `phone` : Téléphone
- `address` : Adresse
- `city`, `country`, `postal_code` : Localisation
- `director_name` : Nom du directeur
- `logo` : Logo de l'école (ImageField)
- `website` : Site web
- `max_students` : Capacité max d'étudiants
- `max_teachers` : Nombre max d'enseignants
- `is_active` : Statut de l'école
- `created_at`, `updated_at` : Dates de création/modification

**Métadonnées:**
- Tri par défaut : `name`
- Recherche disponible sur : `name`, `code`, `email`, `director_name`, `city`
- Filtrage par : `is_active`, `created_at`, `country`, `city`

### 2. CustomUser (Utilisateur Personnalisé)

Utilisateur personnalisé héritant de `AbstractUser` avec rôles et association à une école.

**Rôles disponibles:**
- `superadmin` : Super Administrateur (gère tout le système)
- `director` : Directeur d'école
- `teacher` : Enseignant
- `accountant` : Comptable
- `student` : Étudiant
- `parent` : Parent

**Champs personnalisés:**
- `school` : ForeignKey vers School (nullable pour les superadmins)
- `role` : Choix parmi les rôles ci-dessus (défaut: student)
- `phone` : Téléphone personnel
- `address`, `city`, `country`, `postal_code` : Adresse personnelle
- `profile_photo` : Photo de profil (ImageField)
- `bio` : Biographie (max 500 caractères)
- `is_verified` : Email vérifié
- `is_banned` : Compte suspendu
- `created_at`, `updated_at` : Dates
- `last_login_at` : Dernière connexion

**Méthodes utiles:**
- `is_superadmin()` : Vérifie si super admin
- `is_director()` : Vérifie si directeur
- `is_teacher()` : Vérifie si enseignant
- `is_accountant()` : Vérifie si comptable
- `is_student()` : Vérifie si étudiant
- `is_parent()` : Vérifie si parent
- `full_address` : Retourne l'adresse complète formatée

**Configuration:**
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

## Admin Django

### SchoolAdmin

Interface d'administration complète pour les écoles avec :

**Affichage en liste:**
- Code et nom de l'école
- Ville
- Nom du directeur
- Nombre d'utilisateurs (champ calculé)
- Badge de statut (Actif/Inactif)
- Date de création

**Groupes de champs (fieldsets):**
1. Informations principales
2. Localisation
3. Administration
4. Capacité
5. Statut
6. Dates (repliable)
7. Statistiques (repliable)

**Filtres:** `is_active`, `created_at`, `country`, `city`

**Recherche:** `name`, `code`, `email`, `director_name`, `city`

### CustomUserAdmin

Interface d'administration avancée pour les utilisateurs avec :

**Affichage en liste:**
- Nom complet (ou username)
- Email
- Lien vers l'école (cliquable)
- Badge du rôle (avec couleurs)
- Badge de vérification (Email)
- Badge de statut
- Dernière connexion

**Groupes de champs:**
1. Informations de connexion
2. Informations personnelles
3. École et Rôle
4. Adresse (repliable)
5. Permissions (repliable)
6. Statut
7. Dates (repliable)

**Filtres:** `role`, `school`, `is_active`, `is_verified`, `is_banned`, `created_at`

**Recherche:** `username`, `first_name`, `last_name`, `email`, `school__name`

**Badges colorés pour les rôles:**
- Super Admin : Rouge
- Directeur : Bleu
- Enseignant : Vert
- Comptable : Orange
- Étudiant : Violet
- Parent : Rose

## Installation et Migrations

### Créer les migrations initiales

```bash
python manage.py makemigrations
```

### Appliquer les migrations

```bash
python manage.py migrate
```

### Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### Charger les données initiales (optionnel)

```bash
python manage.py loaddata initial_data.json
```

## Bonnes pratiques

### 1. Vérification des rôles

Au lieu d'utiliser des strings, utilisez les méthodes utilitaires :

```python
# ❌ Mauvais
if user.role == 'teacher':
    pass

# ✓ Bon
if user.is_teacher():
    pass
```

### 2. Filtres personnalisés

```python
# Tous les enseignants d'une école
teachers = CustomUser.objects.filter(school=school, role='teacher')

# Tous les utilisateurs vérifiés et actifs
active_users = CustomUser.objects.filter(is_active=True, is_verified=True)

# Super admins uniquement
super_admins = CustomUser.objects.filter(role='superadmin')
```

### 3. Requêtes optimisées

```python
# Avec select_related pour ForeignKey
users = CustomUser.objects.select_related('school').all()

# Avec prefetch_related pour reverse relationships
schools = School.objects.prefetch_related('users').all()
```

### 4. Permissions personnalisées

Pour ajouter des permissions personnalisées, vous pouvez créer une permission dans le modèle :

```python
class Meta:
    permissions = [
        ('can_approve_grades', 'Can approve grades'),
        ('can_view_reports', 'Can view reports'),
    ]
```

## API Endpoints (à implémenter)

### Écoles
- `GET /api/v1/schools/` - Lister toutes les écoles
- `GET /api/v1/schools/{id}/` - Détail d'une école
- `POST /api/v1/schools/` - Créer une école (SuperAdmin seulement)
- `PUT /api/v1/schools/{id}/` - Modifier une école
- `DELETE /api/v1/schools/{id}/` - Supprimer une école

### Utilisateurs
- `GET /api/v1/users/` - Lister les utilisateurs
- `GET /api/v1/users/{id}/` - Détail d'un utilisateur
- `POST /api/v1/users/` - Créer un utilisateur
- `PUT /api/v1/users/{id}/` - Modifier un utilisateur
- `DELETE /api/v1/users/{id}/` - Supprimer un utilisateur
- `POST /api/v1/users/change-password/` - Changer le mot de passe

### Authentification
- `POST /api/v1/auth/login/` - Connexion
- `POST /api/v1/auth/logout/` - Déconnexion
- `POST /api/v1/auth/refresh-token/` - Rafraîchir le token
- `GET /api/v1/auth/me/` - Récupérer le profil courant

## Signaux Django (à implémenter)

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Créer un profil utilisateur ou envoyer un email de bienvenue
        pass
```

## Tâches Celery (à implémenter)

```python
from celery import shared_task

@shared_task
def send_verification_email(user_id):
    user = CustomUser.objects.get(id=user_id)
    # Envoyer un email de vérification
    pass

@shared_task
def generate_school_report(school_id):
    school = School.objects.get(id=school_id)
    # Générer un rapport pour l'école
    pass
```

## Prochaines étapes

1. ✓ Créer les modèles School et CustomUser
2. ✓ Configurer AUTH_USER_MODEL
3. ✓ Créer l'admin personnalisé
4. ⏭ Créer les serializers DRF
5. ⏭ Créer les views et viewsets
6. ⏭ Ajouter les permissions personnalisées
7. ⏭ Implémenter l'authentification (JWT ou Token)
8. ⏭ Ajouter les validations personnalisées
9. ⏭ Créer les tests unitaires
10. ⏭ Ajouter les signaux Django
11. ⏭ Implémenter les tâches Celery

---

**App accounts prête pour l'intégration avec les autres apps!**
