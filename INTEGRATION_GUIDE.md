# 📌 INTÉGRATION COMPLÈTE - MODELS.PY + ADMIN.PY + SETTINGS.PY

## 1️⃣ MODELS.PY - La structure des données

```python
# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class School(models.Model):
    """Modèle de l'école"""
    name = models.CharField(_("Nom de l'école"), max_length=255, unique=True)
    code = models.CharField(_("Code"), max_length=50, unique=True)
    email = models.EmailField(_("Email"), unique=True)
    # ... autres champs
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class CustomUser(AbstractUser):
    """Utilisateur personnalisé avec rôles"""
    
    ROLE_CHOICES = [
        ('superadmin', _('Super Admin')),
        ('director', _('Directeur')),
        ('teacher', _('Enseignant')),
        ('accountant', _('Comptable')),
        ('student', _('Étudiant')),
        ('parent', _('Parent')),
    ]
    
    school = models.ForeignKey(School, on_delete=models.PROTECT, ...)
    role = models.CharField(_("Rôle"), max_length=20, choices=ROLE_CHOICES, ...)
    # ... autres champs
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
```

**Points clés:**
- CustomUser hérite de `AbstractUser`
- Relation ForeignKey vers School
- Rôles avec choix
- Méthodes de vérification de rôle

---

## 2️⃣ ADMIN.PY - L'interface d'administration

```python
# apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """Admin pour School"""
    list_display = ['code', 'name', 'user_count', 'is_active_badge']
    fieldsets = (
        ("Informations", {'fields': ('name', 'code', 'email')}),
        ("Localisation", {'fields': ('address', 'city', 'country')}),
        # ...
    )
    
    def user_count(self, obj):
        return obj.users.count()

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin pour CustomUser"""
    list_display = ['get_full_name_display', 'email', 'school_link', 'get_role_badge']
    fieldsets = (
        ("Connexion", {'fields': ('username', 'email', 'password')}),
        ("Personnel", {'fields': ('first_name', 'last_name', 'phone')}),
        ("École/Rôle", {'fields': ('school', 'role')}),
        # ...
    )
    
    def get_role_badge(self, obj):
        colors = {
            'teacher': '#388e3c',
            'director': '#1976d2',
            # ...
        }
        color = colors.get(obj.role, '#666')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px;">{}</span>',
            color,
            obj.get_role_display()
        )
```

**Points clés:**
- Hérite de `BaseUserAdmin` pour CustomUser
- Affiche les données pertinentes
- Badges colorés pour les rôles
- Fieldsets organisés
- Filtres et recherche

---

## 3️⃣ SETTINGS.PY - La configuration Django

```python
# school_management/settings.py

# ========== INSTALLED APPS ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'django_filters',
    
    # Local - IMPORTANT: apps.accounts en premier
    'apps.accounts',
]

# ========== AUTHENTICATION ==========
# ⚠️ CRUCIAL: Dire à Django d'utiliser CustomUser
AUTH_USER_MODEL = 'accounts.CustomUser'

# Validateurs de mot de passe
AUTH_PASSWORD_VALIDATORS = [
    # ... validateurs
]

# ========== DATABASE ==========
# Support de SQLite (dev) et PostgreSQL (prod)
if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:  # PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            # ... autres paramètres
        }
    }

# ========== INTERNATIONALIZATION ==========
LANGUAGE_CODE = 'fr-fr'  # Pour les traductions admin
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True
```

**Points clés:**
- `AUTH_USER_MODEL = 'accounts.CustomUser'` ESSENTIEL
- `apps.accounts` dans INSTALLED_APPS
- Support SQLite et PostgreSQL

---

## 🔄 Comment tout s'intègre

### 1️⃣ Django lit `settings.py`
```
settings.py
    ↓
AUTH_USER_MODEL = 'accounts.CustomUser'
    ↓
INSTALLED_APPS = ['apps.accounts']
```

### 2️⃣ Django charge `models.py`
```
Django scrape les modèles
    ↓
Trouve School et CustomUser
    ↓
School → Table "accounts_school"
CustomUser → Table "accounts_customuser" (replaces django.contrib.auth.User)
```

### 3️⃣ Django crée `migrations`
```
python manage.py makemigrations
    ↓
Crée apps/accounts/migrations/0001_initial.py
    ↓
Contient les opérations :
    - CreateModel 'School'
    - CreateModel 'CustomUser'
```

### 4️⃣ Appliquer les migrations
```
python manage.py migrate
    ↓
Exécute les SQL :
    - CREATE TABLE accounts_school
    - CREATE TABLE accounts_customuser
```

### 5️⃣ Django charge `admin.py`
```
Django scrape admin.py
    ↓
Enregistre SchoolAdmin et CustomUserAdmin
    ↓
Admin interface disponible à /admin
```

### 6️⃣ Dans les vues
```python
from apps.accounts.models import CustomUser

@login_required
def my_view(request):
    user = request.user  # Type: CustomUser (pas User)
    
    # Accès aux champs personnalisés
    if user.is_teacher():
        # Logique pour les enseignants
        pass
    
    # Accès à l'école
    school = user.school
```

---

## 📋 Checklist de synchronisation

Avant de démarrer, vérifier que tout est synchronisé :

```bash
# 1. ✓ AUTH_USER_MODEL dans settings.py
grep "AUTH_USER_MODEL" school_management/settings.py
# Doit afficher: AUTH_USER_MODEL = 'accounts.CustomUser'

# 2. ✓ apps.accounts dans INSTALLED_APPS
grep -A 15 "INSTALLED_APPS = " school_management/settings.py
# Doit contenir: 'apps.accounts'

# 3. ✓ models.py existe
ls -la apps/accounts/models.py

# 4. ✓ admin.py existe
ls -la apps/accounts/admin.py

# 5. ✓ CustomUser hérite de AbstractUser
grep "class CustomUser" apps/accounts/models.py
# Doit montrer: class CustomUser(AbstractUser):

# 6. ✓ CustomUser est enregistré dans admin
grep "@admin.register(CustomUser)" apps/accounts/admin.py

# 7. ✓ Vérifier les migrations
python manage.py showmigrations accounts
```

---

## ⚠️ Erreurs communes et solutions

### Erreur: "The installed auth app doesn't have the 'auth_user' permission"

**Cause**: AUTH_USER_MODEL est défini après les migrations

**Solution**:
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'apps.accounts',  # ✓ Après 'auth'
]

AUTH_USER_MODEL = 'accounts.CustomUser'  # ✓ En bas
```

### Erreur: "Substituting a custom User model has side effects"

**Cause**: Les migrations ont déjà créé la table User par défaut

**Solution**: Nettoyer et recommencer
```bash
# ATTENTION: Perte de données!
python manage.py flush
python manage.py migrate
```

### Erreur: "ForeignKey to unswapped model 'auth.User'"

**Cause**: Un modèle référence User au lieu de CustomUser

**Solution**:
```python
# ❌ Mauvais
school = models.ForeignKey(User, ...)

# ✓ Bon
school = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
```

### Erreur: "relation 'auth_user' does not exist"

**Cause**: Les migrations ne sont pas appliquées

**Solution**:
```bash
python manage.py migrate
```

---

## 🎯 Flux complet de démarrage

### Step 1: Configuration (settings.py)
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
INSTALLED_APPS = ['apps.accounts', ...]
```

### Step 2: Modèles (models.py)
```python
class School(models.Model): ...
class CustomUser(AbstractUser): ...
```

### Step 3: Admin (admin.py)
```python
@admin.register(School)
class SchoolAdmin: ...

@admin.register(CustomUser)
class CustomUserAdmin: ...
```

### Step 4: Migrations
```bash
python manage.py makemigrations
```

### Step 5: Appliquer les migrations
```bash
python manage.py migrate
```

### Step 6: Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### Step 7: Accéder à l'admin
```
http://localhost:8000/admin
```

---

## ✅ Vérification finale

Une fois tout en place, vérifier :

```bash
# 1. Pas d'erreurs
python manage.py check

# 2. Migrations appliquées
python manage.py showmigrations accounts
# Doit afficher [X] pour toutes les migrations

# 3. Créer un utilisateur par l'admin
# http://localhost:8000/admin → CustomUser → Add

# 4. Vérifier dans le shell
python manage.py shell
```

```python
from django.contrib.auth import get_user_model

User = get_user_model()
print(User)  # Doit afficher: <class 'apps.accounts.models.CustomUser'>

# Créer un utilisateur
user = User.objects.create_user(
    username='test',
    email='test@example.com',
    password='testpass123'
)

print(user.is_teacher())  # Doit fonctionner
```

---

**Tout est maintenant intégré et prêt à fonctionner!** 🚀
