# App Students - Documentation Complète

## Vue d'ensemble

L'app `students` gère les élèves d'une école avec un CRUD complet, recherche, filtrage et protection par école.

## Structure des fichiers

```
apps/students/
├── __init__.py
├── models.py              # Modèle Student
├── views.py              # Vues (CRUD, recherche, etc.)
├── forms.py              # Formulaires Django
├── urls.py               # Routes URL
├── admin.py              # Admin Django
├── tests.py              # Tests unitaires
├── apps.py               # Configuration de l'app
└── migrations/
    └── __init__.py
```

## Installation

### 1. Ajouter l'app à INSTALLED_APPS

**Fichier:** `school_management/settings.py`

```python
INSTALLED_APPS = [
    # ...
    'apps.students',
]
```

### 2. Ajouter les URLs

**Fichier:** `school_management/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('students/', include('apps.students.urls')),  # <-- Ajouter cette ligne
]
```

### 3. Créer les migrations

```bash
python manage.py makemigrations students
python manage.py migrate students
```

## Modèle Student

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `first_name` | CharField | Prénom de l'élève |
| `last_name` | CharField | Nom de l'élève |
| `student_id` | CharField | Numéro unique d'élève (ex: STU-2024-001) |
| `school` | ForeignKey | École de l'élève |
| `grade` | CharField | Classe/Niveau (ex: 6ème A) |
| `date_of_birth` | DateField | Date de naissance |
| `gender` | CharField | Genre (M, F, O) |
| `email` | EmailField | Email personnel (optional) |
| `phone` | CharField | Téléphone (optional) |
| `address` | TextField | Adresse (optional) |
| `city` | CharField | Ville (optional) |
| `postal_code` | CharField | Code postal (optional) |
| `country` | CharField | Pays (optional) |
| `parent_name` | CharField | Nom du parent/tuteur |
| `parent_phone` | CharField | Téléphone du parent |
| `parent_email` | EmailField | Email du parent |
| `enrollment_date` | DateField | Date d'inscription (auto) |
| `gpa` | DecimalField | Moyenne générale (0-20) |
| `photo` | ImageField | Photo de profil |
| `status` | CharField | Statut (active, inactive, graduated, suspended) |
| `notes` | TextField | Notes supplémentaires |
| `created_at` | DateTimeField | Date de création (auto) |
| `updated_at` | DateTimeField | Date de modification (auto) |

### Propriétés utiles

```python
@property
def full_name(self):
    """Retour: "Prénom Nom" """
    return f"{self.first_name} {self.last_name}"

@property
def age(self):
    """Calcule l'âge en années"""
    
@property
def full_address(self):
    """Adresse complète formatée"""
    
def is_active_student(self):
    """True si le statut est 'active'"""
    
def can_enroll(self):
    """True si l'élève peut s'inscrire"""
```

## Vues (Views)

### Liste des élèves
```
URL: /students/
Nom: students:student_list
Méthode: GET
Paramètres GET:
  - search: Rechercher par nom/numéro
  - grade: Filtrer par classe
  - status: Filtrer par statut
  - gender: Filtrer par genre
  - sort_by: Tri (last_name, first_name, gpa, etc.)
  - page: Numéro de page
```

### Détail d'un élève
```
URL: /students/<id>/
Nom: students:student_detail
Méthode: GET
```

### Créer un élève
```
URL: /students/create/
Nom: students:student_create
Méthode: GET/POST
Permissions: director, superadmin
```

### Modifier un élève
```
URL: /students/<id>/edit/
Nom: students:student_edit
Méthode: GET/POST
Permissions: director, superadmin
```

### Supprimer un élève
```
URL: /students/<id>/delete/
Nom: students:student_delete
Méthode: GET/POST
Permissions: director, superadmin
```

### Recherche AJAX
```
URL: /students/search/?q=texte
Nom: students:student_search
Méthode: GET
Retour: JSON
```

### Exporter en CSV
```
URL: /students/export/
Nom: students:student_export
Méthode: GET
Retour: CSV file
```

### Actions en masse
```
URL: /students/bulk-action/
Nom: students:student_bulk_action
Méthode: POST
Actions: activate, deactivate, graduate, suspend
```

### Statistiques
```
URL: /students/statistics/
Nom: students:student_statistics
Méthode: GET
```

## Formulaires

### StudentForm
Formulaire complet pour créer/modifier un élève avec validation.

```python
from apps.students.forms import StudentForm

form = StudentForm(data=request.POST, files=request.FILES)
if form.is_valid():
    student = form.save()
```

### StudentSearchForm
Formulaire pour les filtres de recherche.

### StudentFilterForm
Formulaire pour les filtres avancés.

## Templates

### student_list.html
Liste paginée des élèves avec recherche et filtres.

### student_detail.html
Profil complet d'un élève.

### student_form.html
Formulaire de création/modification.

### student_confirm_delete.html
Confirmation avant suppression.

### student_statistics.html
Statistiques et graphiques des élèves.

## Protection des données

### Isolation par école

Chaque utilisateur ne voit que les élèves de son école:

```python
if request.user.is_superuser or request.user.role == 'superadmin':
    students = Student.objects.all()
else:
    if request.user.school:
        students = request.user.school.students.all()
    else:
        students = Student.objects.none()
```

### Permissions

- **SuperAdmin/Director**: Accès complet
- **Teacher**: Accès lecture uniquement
- **Student/Parent**: Accès à son propre profil
- **Accountant**: Accès lecture pour les rapports

## Exemples d'utilisation

### Créer un élève

```python
from apps.students.models import Student

student = Student.objects.create(
    first_name='Jean',
    last_name='Dupont',
    student_id='STU-2024-001',
    school=school_obj,
    grade='6ème A',
    date_of_birth=date(2010, 5, 15),
    gender='M',
    status='active',
    parent_name='Marie Dupont',
    parent_email='parent@email.com'
)
```

### Récupérer les élèves actifs d'une classe

```python
active_students = school.students.filter(
    grade='6ème A',
    status='active'
).order_by('last_name')
```

### Filtrer par moyenne

```python
excellent_students = Student.objects.filter(
    gpa__gte=16
).order_by('-gpa')

struggling_students = Student.objects.filter(
    gpa__lt=10
)
```

### Exporter les élèves

```python
# Via l'interface: /students/export/
# Génère un fichier CSV téléchargeable
```

## Statistiques disponibles

- Total des élèves
- Élèves actifs/inactifs
- Élèves diplômés
- Élèves suspendus
- Répartition par classe
- Moyenne générale

## Filtres et recherche

### Recherche par
- Prénom
- Nom
- Numéro d'élève
- Email

### Filtres par
- Classe/Niveau
- Statut (active, inactive, graduated, suspended)
- Genre
- Moyenne générale

### Tri par
- Nom (A-Z ou Z-A)
- Prénom
- Moyenne générale
- Date d'inscription

## Admin Django

L'interface admin personnalisée offre:

- Affichage coloré des statuts
- Badges de moyenne générale
- Filtres avancés
- Actions en masse (Activer, Désactiver, Diplômer, Suspendre)
- Export des données

```bash
python manage.py runserver
# Aller à: http://localhost:8000/admin/
```

## Tests

Exécuter les tests:

```bash
python manage.py test apps.students
```

Tests inclus:
- Création d'élève
- Unicité du numéro
- Calcul de l'âge
- Adresse complète
- Vues CRUD
- Isolation par école
- Recherche et filtrage

## Bonus: Commande de management

Créer des élèves de test:

```bash
python manage.py shell
```

```python
from apps.students.models import Student
from apps.accounts.models import School
from datetime import date

school = School.objects.first()

for i in range(10):
    Student.objects.create(
        first_name=f'Élève{i}',
        last_name=f'Test{i}',
        student_id=f'STU-2024-{i:03d}',
        school=school,
        grade='6ème A',
        date_of_birth=date(2010, 1, 1),
        status='active'
    )
```

## Notes de performance

- Indexation sur (school, grade) et (school, status)
- Pagination de 15 élèves par page
- Requêtes optimisées avec select_related/prefetch_related si nécessaire
- Recherche en texte intégral possible avec PostgreSQL (à implémenter)

## Évolutions futures

- [ ] Import CSV d'élèves
- [ ] Génération de cartes d'identification
- [ ] Intégration avec classes/cours
- [ ] Suivi des absences
- [ ] Carnet de notes
- [ ] Communications parent/école
- [ ] Documents (certificats, relevés)
- [ ] Rapports personnalisés

