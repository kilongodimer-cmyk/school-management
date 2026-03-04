# Guide d'intégration - App Students

## Étape 1: Ajouter l'app aux INSTALLED_APPS

**Fichier**: `school_management/settings.py`

Localiser la liste `INSTALLED_APPS` et ajouter `'apps.students'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    
    'apps.accounts',
    'apps.students',  # ← AJOUTER CETTE LIGNE
]
```

## Étape 2: Ajouter les URLs

**Fichier**: `school_management/urls.py`

Localiser la liste `urlpatterns` et ajouter la route pour students:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('students/', include('apps.students.urls')),  # ← AJOUTER CETTE LIGNE
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Étape 3: Appliquer les migrations

Dans votre terminal:

```bash
# Créer les migrations
python manage.py makemigrations

# Afficher les migrations à appliquer
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate
```

Résultat attendu:
```
Running migrations:
  Applying students.0001_initial... OK
```

## Étape 4: Vérifier l'installation

Tester que tout fonctionne:

```bash
# Lancer le serveur
python manage.py runserver

# Ouvrir http://localhost:8000/students/
# Vous devriez voir "Gestion des Élèves"
```

## Étape 5: Créer des données de test (optionnel)

```bash
python manage.py shell
```

```python
from apps.students.models import Student
from apps.accounts.models import School
from datetime import date

# Récupérer une école
school = School.objects.first()

# Créer quelques élèves
for i in range(10):
    Student.objects.create(
        first_name=f'Élève{i}',
        last_name=f'Test{i}',
        student_id=f'STU-2024-{i:03d}',
        school=school,
        grade='6ème A' if i < 5 else '6ème B',
        date_of_birth=date(2010, 1, 1),
        gender='M' if i % 2 == 0 else 'F',
        parent_name=f'Parent {i}',
        parent_email=f'parent{i}@test.com',
        status='active'
    )

print("✅ 10 élèves créés")

# Quitter le shell
exit()
```

## Étape 6: Accéder aux interfaces

### Interface Web
```
Accueil: http://localhost:8000/students/
```

### Admin Django
```
Admin: http://localhost:8000/admin/
Rechercher: Gestion des Élèves
```

## Structure d'intégration

```
school_management/
├── school_management/
│   ├── settings.py          ← Ajouter 'apps.students'
│   ├── urls.py              ← Ajouter la route students
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── accounts/            ← App existante
│   │   ├── models.py        (School, CustomUser)
│   │   ├── views.py
│   │   └── ...
│   │
│   └── students/            ← Nouvelle app
│       ├── models.py        (Student)
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       ├── admin.py
│       ├── tests.py
│       └── migrations/
│
├── templates/
│   ├── accounts/
│   │   └── ...
│   │
│   └── students/            ← Nouveaux templates
│       ├── student_list.html
│       ├── student_detail.html
│       ├── student_form.html
│       ├── student_confirm_delete.html
│       └── student_statistics.html
│
└── manage.py
```

## Navigation du menu

Ajouter un lien dans `templates/accounts/base.html` pour accéder à l'app:

```html
<!-- Dans la sidebar ou le menu principal -->
<li class="nav-item">
    <a class="nav-link" href="{% url 'students:student_list' %}">
        <i class="fas fa-graduation-cap"></i>
        <span>Élèves</span>
    </a>
</li>
```

Depuis le template `base.html` existant:

**Fichier**: `templates/accounts/base.html`

Localiser le sidebar et ajouter dans la navigation:

```html
<!-- Existant -->
<a class="nav-link" href="{% url 'accounts:dashboard' %}">
    <i class="fas fa-chart-line"></i> Dashboard
</a>

<!-- Ajouter après -->
<a class="nav-link" href="{% url 'students:student_list' %}">
    <i class="fas fa-graduation-cap"></i> Élèves
</a>
```

## Accès aux permissions

### Pour un directeur

1. Se connecter avec un compte directeur
2. Aller à `/students/`
3. Voir uniquement les élèves de son école

### Pour un super admin

1. Se connecter avec un compte superadmin
2. Aller à `/students/`
3. Voir tous les élèves

### Pour un enseignant

1. Se connecter avec un compte professeur
2. Aller à `/students/`
3. Voir les élèves (lecture uniquement)

## Dépannage d'intégration

### Erreur: "No module named 'students'"

```bash
# Solution: Assurez-vous que INSTALLED_APPS contient 'apps.students'
python manage.py check
```

### Erreur: "students.Student table does not exist"

```bash
# Solution: Appliquer les migrations
python manage.py migrate
```

### Erreur: "Reverse for 'student_list' not found"

```bash
# Solution: Vérifier que les URLs sont ajoutées
python manage.py show_urls | grep student
```

### Les élèves ne s'affichent pas

```python
# Vérifier en shell
from apps.students.models import Student
print(Student.objects.count())  # Devrait être > 0
```

### Permission denied sur les actions

```python
# Vérifier le rôle de l'utilisateur
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='votre_user')
print(user.role)  # Doit être 'director' ou 'superadmin'
```

## Vérification post-installation

Checklist de vérification:

- [ ] App ajoutée à INSTALLED_APPS
- [ ] URLs ajoutées à urlpatterns
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Page `/students/` accessible
- [ ] Admin accessible à `/admin/`
- [ ] Message de bienvenue visible ("Gestion des Élèves")
- [ ] Formulaires de création fonctionnels
- [ ] Filtres et recherche fonctionnels
- [ ] Permissions respectées par rôle
- [ ] Isolation école fonctionne

## Intégration avec les données existantes

Vous pouvez exploiter les données School existantes:

```python
from apps.accounts.models import School
from apps.students.models import Student

# Lister les écoles
for school in School.objects.all():
    print(f"{school.name}: {school.students.count()} élèves")

# Accéder aux élèves d'une école
school = School.objects.first()
print(school.students.all())  # Queryset des élèves
```

## Prochaines étapes

Après une intégration réussie:

1. **Ajouter des élèves**
   - Créer un formulaire en lot
   - Importer depuis CSV
   - API d'ajout automatique

2. **Personnaliser**
   - Ajouter des champs au modèle
   - Modifier les templates
   - Ajouter des validations

3. **Intégrer avec d'autres apps**
   - App Courses (Cours)
   - App Grades (Notes)
   - App Attendance (Absences)

4. **Améliorer la sécurité**
   - Audit logging
   - Versioning des données
   - Backup automatique

5. **Optimiser les performances**
   - Ajout de caching
   - Indexation supplémentaire
   - Recherche full-text

## Support

Questions fréquentes:

**Q: Comment changer le nombre d'élèves par page?**
```python
# Dans views.py, fonction student_list()
paginator = Paginator(students, 30)  # Au lieu de 15
```

**Q: Comment ajouter un nouveau champ?**
```python
# Dans models.py, ajouter au modèle
ma_propriete = models.CharField(max_length=100)

# Créer une migration
python manage.py makemigrations
python manage.py migrate
```

**Q: Comment modifier le tri par défaut?**
```python
# Dans models.py, Meta class
class Meta:
    ordering = ['grade', 'last_name']  # Tri par classe puis nom
```

**Q: Comment exporter plus de colonnes en CSV?**
```python
# Dans views.py, fonction student_export_list()
writer.writerow([...champs supplémentaires...])
```

---

**Intégration complète**: 15 minutes ⏱️  
**Statut**: ✅ Ready to use
