# 🎯 LES 3 FICHIERS CLÉS - RÉSUMÉ COMPLET

## 📌 Demande du projet

**Créer une app Django appelée accounts avec :**
- ✅ Modèle School
- ✅ Modèle CustomUser héritant de AbstractUser
- ✅ Chaque utilisateur appartient à une école
- ✅ Rôles : SuperAdmin, Directeur, Enseignant, Comptable
- ✅ AUTH_USER_MODEL configuré
- ✅ Admin personnalisé
- ✅ Migration complète

---

## 1️⃣ MODELS.PY

### Fichier: `apps/accounts/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class School(models.Model):
    """Modèle pour représenter une école"""
    
    name = models.CharField(
        _("Nom de l'école"),
        max_length=255,
        unique=True,
    )
    
    code = models.CharField(
        _("Code de l'école"),
        max_length=50,
        unique=True,
    )
    
    email = models.EmailField(
        _("Email de l'école"),
        unique=True,
    )
    
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
        blank=True,
        null=True,
    )
    
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    director_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='schools/logos/%Y/%m/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    max_students = models.IntegerField(default=1000)
    max_teachers = models.IntegerField(default=100)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("École")
        verbose_name_plural = _("Écoles")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class CustomUser(AbstractUser):
    """Utilisateur personnalisé héritant de AbstractUser"""
    
    ROLE_CHOICES = [
        ('superadmin', _('Super Admin')),
        ('director', _('Directeur')),
        ('teacher', _('Enseignant')),
        ('accountant', _('Comptable')),
        ('student', _('Étudiant')),
        ('parent', _('Parent')),
    ]

    # Relation avec School
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True,
        verbose_name=_("École"),
    )

    # Rôle de l'utilisateur
    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
    )

    # Informations supplémentaires
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    profile_photo = models.ImageField(
        upload_to='users/profiles/%Y/%m/',
        blank=True,
        null=True,
    )
    bio = models.TextField(max_length=500, blank=True, null=True)

    # Statuts
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['school', 'role']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    # Méthodes de vérification de rôle
    def is_superadmin(self):
        return self.role == 'superadmin' or self.is_superuser

    def is_director(self):
        return self.role == 'director'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_accountant(self):
        return self.role == 'accountant'

    def is_student(self):
        return self.role == 'student'

    def is_parent(self):
        return self.role == 'parent'

    @property
    def full_address(self):
        """Retourne l'adresse complète formatée"""
        parts = [self.address, self.postal_code, self.city, self.country]
        return ', '.join([p for p in parts if p])
```

**Points clés :**
- ✅ School avec tous les champs nécessaires
- ✅ CustomUser hérite de AbstractUser
- ✅ Relation ForeignKey School → CustomUser
- ✅ Rôles: superadmin, director, teacher, accountant, student, parent
- ✅ Méthodes de vérification de rôle
- ✅ Index pour performances

---

## 2️⃣ ADMIN.PY

### Fichier: `apps/accounts/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import School, CustomUser


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """Admin personnalisé pour School"""
    
    list_display = [
        'code',
        'name',
        'city',
        'director_name',
        'user_count',
        'is_active_badge',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'created_at',
        'country',
        'city'
    ]
    
    search_fields = [
        'name',
        'code',
        'email',
        'director_name',
        'city'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'user_count'
    ]
    
    fieldsets = (
        (_("Informations principales"), {
            'fields': ('name', 'code', 'email', 'phone', 'website')
        }),
        (_("Localisation"), {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        (_("Administration"), {
            'fields': ('director_name', 'logo')
        }),
        (_("Capacité"), {
            'fields': ('max_students', 'max_teachers')
        }),
        (_("Statut"), {
            'fields': ('is_active',)
        }),
        (_("Dates"), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        (_("Statistiques"), {
            'fields': ('user_count',),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    def user_count(self, obj):
        """Nombre d'utilisateurs"""
        count = obj.users.count()
        return format_html('<strong>{}</strong>', count)
    user_count.short_description = _("Nombre d'utilisateurs")
    
    def is_active_badge(self, obj):
        """Badge de statut"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Actif</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Inactif</span>'
        )
    is_active_badge.short_description = _("Statut")


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin personnalisé pour CustomUser"""
    
    list_display = [
        'get_full_name_display',
        'email',
        'school_link',
        'get_role_badge',
        'is_verified_badge',
        'is_active_badge',
        'last_login'
    ]
    
    list_filter = [
        'role',
        'school',
        'is_active',
        'is_verified',
        'is_banned',
        'created_at',
    ]
    
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'school__name'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'last_login_at',
        'get_role_display_fr'
    ]
    
    fieldsets = (
        (_("Informations de connexion"), {
            'fields': ('username', 'email', 'password')
        }),
        (_("Informations personnelles"), {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'profile_photo',
                'bio'
            )
        }),
        (_("École et Rôle"), {
            'fields': ('school', 'role', 'get_role_display_fr')
        }),
        (_("Adresse"), {
            'fields': (
                'address',
                'postal_code',
                'city',
                'country'
            ),
            'classes': ('collapse',)
        }),
        (_("Permissions"), {
            'fields': (
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_("Statut"), {
            'fields': (
                'is_active',
                'is_verified',
                'is_banned'
            )
        }),
        (_("Dates"), {
            'fields': (
                'created_at',
                'updated_at',
                'last_login_at',
                'last_login'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'school',
                'role'
            ),
        }),
    )
    
    ordering = ['-created_at']
    filter_horizontal = ['groups', 'user_permissions']
    
    def get_full_name_display(self, obj):
        """Nom complet ou username"""
        full_name = obj.get_full_name()
        return full_name if full_name.strip() else obj.username
    get_full_name_display.short_description = _("Utilisateur")
    
    def school_link(self, obj):
        """Lien vers l'école"""
        if obj.school:
            url = f'/admin/accounts/school/{obj.school.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.school.name)
        return format_html('<em style="color: gray;">-</em>')
    school_link.short_description = _("École")
    
    def get_role_badge(self, obj):
        """Badge coloré du rôle"""
        colors = {
            'superadmin': '#d32f2f',
            'director': '#1976d2',
            'teacher': '#388e3c',
            'accountant': '#f57c00',
            'student': '#7b1fa2',
            'parent': '#c2185b',
        }
        color = colors.get(obj.role, '#666')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 4px; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    get_role_badge.short_description = _("Rôle")
    
    def is_verified_badge(self, obj):
        """Badge de vérification"""
        if obj.is_verified:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Vérifié</span>'
            )
        return format_html(
            '<span style="color: orange;">⧖ Non vérifié</span>'
        )
    is_verified_badge.short_description = _("Vérification")
    
    def is_active_badge(self, obj):
        """Badge de statut"""
        if obj.is_banned:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Suspendu</span>'
            )
        if obj.is_active:
            return format_html(
                '<span style="color: green;">✓ Actif</span>'
            )
        return format_html(
            '<span style="color: gray;">✗ Inactif</span>'
        )
    is_active_badge.short_description = _("Statut")
```

**Points clés :**
- ✅ SchoolAdmin avec list_display, fieldsets, filtres, recherche
- ✅ CustomUserAdmin héritant de BaseUserAdmin
- ✅ Badges colorés pour les 6 rôles
- ✅ Lien cliquable vers l'école
- ✅ Affichage intelligent des statuts
- ✅ Readonly fields intelligents

---

## 3️⃣ SETTINGS.PY (MODIFIÉ)

### Section à ajouter dans `school_management/settings.py`

```python
# ========== INSTALLED APPS ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'django_filters',
    
    # ✅ Local apps - IMPORTANT: apps.accounts ici
    'apps.accounts',
    # 'apps.students',
    # 'apps.teachers',
    # 'apps.courses',
    # 'apps.grades',
]

# ========== CUSTOM USER MODEL ==========
# ⚠️ ESSENTIEL: Configurer le modèle utilisateur personnalisé
AUTH_USER_MODEL = 'accounts.CustomUser'

# ========== DATABASE ==========
# Flexible pour SQLite (dev) et PostgreSQL (prod)
DB_ENGINE = env('DB_ENGINE', default='django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:  # PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': env('DB_NAME', default='school_management_db'),
            'USER': env('DB_USER', default='postgres'),
            'PASSWORD': env('DB_PASSWORD', default=''),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env('DB_PORT', default=5432),
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 600,
        }
    }

# ========== PASSWORD VALIDATION ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========== INTERNATIONALIZATION ==========
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True
```

**Points clés :**
- ✅ `AUTH_USER_MODEL = 'accounts.CustomUser'` CONFIGURÉ
- ✅ `apps.accounts` dans INSTALLED_APPS
- ✅ Flexible pour SQLite/PostgreSQL
- ✅ Password validators robustes
- ✅ Internationalization en français

---

## 🎬 Commandes à exécuter

```bash
# 1. Créer les migrations
python manage.py makemigrations

# 2. Appliquer les migrations
python manage.py migrate

# 3. Créer un superutilisateur
python manage.py createsuperuser

# 4. Lancer le serveur
python manage.py runserver

# 5. Accéder à l'admin
# http://localhost:8000/admin
```

---

## ✅ Vérification finale

```python
# Dans le shell Django
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()

# Doit afficher: <class 'apps.accounts.models.CustomUser'>
print(User)

# Créer un utilisateur
user = User.objects.create_user(
    username='test',
    email='test@example.com',
    password='testpass123'
)

# Vérifier les méthodes de rôle
print(user.is_teacher())  # False
user.role = 'teacher'
user.save()
print(user.is_teacher())  # True
```

---

**Ces 3 fichiers font fonctionner l'app accounts complètement !** 🚀
