# Structure recommandée pour les applications

Après avoir exécuté l'installation, créez les applications Django comme suit :

## Créer la structure des apps

```bash
# Créer le dossier apps
mkdir apps
cd apps
touch __init__.py

# Créer les applications
python ../manage.py startapp users
python ../manage.py startapp schools
python ../manage.py startapp students
python ../manage.py startapp teachers
python ../manage.py startapp courses
python ../manage.py startapp grades
```

## Structure de chaque app

```
apps/
├── __init__.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py              # Configuration admin
│   ├── apps.py               # Configuration app
│   ├── models.py             # Modèles (User, Profile, etc.)
│   ├── views.py              # ViewSets pour API
│   ├── serializers.py        # Serializers DRF
│   ├── urls.py               # Routes de l'app
│   ├── forms.py              # Formulaires (optionnel)
│   ├── tests.py              # Tests unitaires
│   └── tasks.py              # Tâches Celery
├── schools/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── tasks.py
├── students/
│   └── (même structure)
├── teachers/
│   └── (même structure)
├── courses/
│   └── (même structure)
└── grades/
    └── (même structure)
```

## Exemple : apps/users/models.py

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('teacher', 'Enseignant'),
        ('student', 'Étudiant'),
        ('parent', 'Parent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    bio = models.TextField(blank=True)
    school = models.ForeignKey('schools.School', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
```

## Exemple : apps/users/admin.py

```python
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'school', 'created_at')
    list_filter = ('role', 'school', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'role', 'school')
        }),
        ('Détails personnels', {
            'fields': ('phone', 'address', 'city', 'country', 'avatar', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## Exemple : apps/users/serializers.py

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'phone', 'address', 'city', 'country', 'avatar', 'bio', 'school', 'created_at']
        read_only_fields = ['id', 'created_at']
```

## Exemple : apps/users/views.py

```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Les utilisateurs ne voient que leur profil
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Récupérer le profil de l'utilisateur connecté"""
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Mettre à jour son propre profil"""
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## Exemple : apps/users/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
```

## Ajouter les apps à settings.py

```python
INSTALLED_APPS = [
    # Django apps
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
    
    # Local apps
    'apps.users',
    'apps.schools',
    'apps.students',
    'apps.teachers',
    'apps.courses',
    'apps.grades',
]
```

## Ajouter les routes à urls.py principal

```python
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # API v1
    path('api/v1/', include('apps.users.urls')),
    # path('api/v1/', include('apps.schools.urls')),
    # path('api/v1/', include('apps.students.urls')),
    # path('api/v1/', include('apps.teachers.urls')),
    # path('api/v1/', include('apps.courses.urls')),
    # path('api/v1/', include('apps.grades.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Créer les migrations et appliquer

```bash
# Créer les migrations pour toutes les apps
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Vérifier les migrations
python manage.py showmigrations
```

## Charger les données initiales (optionnel)

Créer un fichier `fixtures/initial_data.json` avec les données par défaut, puis :

```bash
python manage.py loaddata initial_data.json
```

---

**Vous avez maintenant une structure complète et modulaire pour développer votre application SaaS !** 🚀
