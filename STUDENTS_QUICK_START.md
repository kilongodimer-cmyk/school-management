# App Students - Guide d'installation et utilisation

## Résumé

L'app **students** fournit un système complet de gestion des élèves avec:

✅ **Modèle Student** complet avec 25+ champs  
✅ **CRUD complet** (Create, Read, Update, Delete)  
✅ **Recherche** par nom/numéro d'élève  
✅ **Filtres** par classe, statut, genre  
✅ **Tri** personnalisable  
✅ **Pagination** 15 élèves par page  
✅ **Protection** - chaque école voit ses élèves uniquement  
✅ **Statistiques** et graphiques  
✅ **Export CSV** des données  
✅ **Templates Bootstrap 5** professionnels  
✅ **Admin Django** personnalisé  
✅ **Tests unitaires** complets  

## Installation rapide

### 1. Les fichiers ont été créés

```
apps/students/
├── __init__.py
├── models.py              # 250+ lignes - Modèle Student complet
├── views.py              # 500+ lignes - 10 vues CRUD + recherche + stats
├── forms.py              # 200+ lignes - 4 formulaires complets
├── urls.py               # Routes pour toutes les vues
├── admin.py              # Interface Admin personnalisée
├── tests.py              # Tests complets
├── apps.py               # Configuration
└── migrations/
    ├── __init__.py
    └── 0001_initial.py   # Migration initiale

templates/students/
├── student_list.html               # Liste avec filtres et pagination
├── student_detail.html             # Profil complet
├── student_form.html               # Formulaire création/modification
├── student_confirm_delete.html     # Confirmation suppression
└── student_statistics.html         # Statistiques et graphiques
```

### 2. Ajouter à settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'apps.accounts',
    'apps.students',    # ← Ajouter cette ligne
]
```

### 3. Ajouter les URLs aux urls principales

**File: `school_management/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('students/', include('apps.students.urls')),  # ← Ajouter cette ligne
]
```

### 4. Appliquer les migrations

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 5. Créer un compte superadmin (facultatif)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

Accéder à:
- **Interface web**: http://localhost:8000/students/
- **Admin Django**: http://localhost:8000/admin/

## URLs disponibles

| URL | Vue | Description |
|-----|-----|-------------|
| `/students/` | student_list | Liste des élèves |
| `/students/<id>/` | student_detail | Détail d'un élève |
| `/students/create/` | student_create | Créer un élève |
| `/students/<id>/edit/` | student_edit | Modifier un élève |
| `/students/<id>/delete/` | student_delete | Supprimer un élève |
| `/students/search/` | student_search | API de recherche AJAX |
| `/students/export/` | student_export | Exporter en CSV |
| `/students/bulk-action/` | student_bulk_action | Actions en masse |
| `/students/statistics/` | student_statistics | Statistiques |

## Modèle Student - Champs

```python
# Identité
- first_name: CharField (Prénom)
- last_name: CharField (Nom)
- student_id: CharField (Unique) (Ex: STU-2024-001)

# École
- school: ForeignKey (School) 
- grade: CharField (Ex: 6ème A, Terminale S)

# Informations personnelles
- date_of_birth: DateField
- gender: CharField (M/F/O)
- email: EmailField (optional)
- phone: CharField (optional)

# Adresse
- address: TextField (optional)
- city: CharField (optional)
- postal_code: CharField (optional)
- country: CharField (optional)

# Parent/Tuteur
- parent_name: CharField (optional)
- parent_phone: CharField (optional)
- parent_email: EmailField (optional)

# Académique
- enrollment_date: DateField (auto)
- gpa: DecimalField (0-20) (optional)
- status: CharField (active/inactive/graduated/suspended)

# Multimédia
- photo: ImageField (optional)

# Divers
- notes: TextField (optional)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
```

## Propriétés utiles

```python
student.full_name              # "Jean Dupont"
student.age                    # 14 (calculé)
student.full_address           # "123 Rue Paix, 75000, Paris, France"
student.is_active_student()    # True/False
student.can_enroll()           # True/False
```

## Exemples de code

### Créer un élève

```python
from apps.students.models import Student
from apps.accounts.models import School
from datetime import date

school = School.objects.get(code='TEST001')

student = Student.objects.create(
    first_name='Jean',
    last_name='Dupont',
    student_id='STU-2024-001',
    school=school,
    grade='6ème A',
    date_of_birth=date(2010, 5, 15),
    gender='M',
    parent_name='Marie Dupont',
    parent_email='parent@email.com',
    status='active'
)
```

### Requêtes utiles

```python
# Élèves actifs
Student.objects.filter(status='active')

# Élèves d'une école
school.students.all()

# Élèves d'une classe
Student.objects.filter(grade='6ème A')

# Excellents résultats
Student.objects.filter(gpa__gte=16).order_by('-gpa')

# À suivre
Student.objects.filter(gpa__lt=10)

# Statistiques
Student.objects.count()
Student.objects.filter(status='active').count()
Student.objects.filter(status='graduated').count()
```

### Utiliser les vues

```python
# Dans templates
{% url 'students:student_list' %}
{% url 'students:student_detail' student.id %}
{% url 'students:student_create' %}
{% url 'students:student_edit' student.id %}
{% url 'students:student_delete' student.id %}

# Dans Python
from django.urls import reverse
reverse('students:student_list')
reverse('students:student_detail', args=[student.id])
```

## Permissions et sécurité

### Isolation par école

✅ Chaque école voit **UNIQUEMENT** ses élèves  
✅ Les directeurs ne peuvent modifier que leurs élèves  
✅ Les élèves voient leurs propres données  

```python
# Protection automatique dans les vues
if request.user.school != student.school:
    messages.error(request, 'Accès refusé')
    return redirect('students:student_list')
```

### Contrôle d'accès par rôle

| Rôle | Liste | Créer | Modifier | Supprimer |
|------|-------|-------|----------|-----------|
| SuperAdmin | ✅ | ✅ | ✅ | ✅ |
| Director | ✅ | ✅ | ✅ | ✅ |
| Teacher | ✅ | ❌ | ❌ | ❌ |
| Accountant | ✅ | ❌ | ❌ | ❌ |
| Student | Propre profil | ❌ | ❌ | ❌ |
| Parent | Propre enfant | ❌ | ❌ | ❌ |

## Admin Django

L'interface admin personnalisée offre:

- ✅ Affichage coloré des statuts
- ✅ Badges pour les moyennes
- ✅ Filtres par école, classe, statut
- ✅ Recherche par nom/email/numéro
- ✅ Actions en masse (Activer, Diplômer, Suspendre)

```bash
python manage.py runserver
# http://localhost:8000/admin/
# Auth > Students > Add Student
```

## Tests

```bash
# Exécuter tous les tests
python manage.py test apps.students

# Avec verbosité
python manage.py test apps.students -v 2

# Test spécifique
python manage.py test apps.students.tests.StudentModelTest
```

Tests inclus:
- ✅ Création de modèle
- ✅ Unicité du numéro
- ✅ Calcul de l'âge
- ✅ CRUD complet
- ✅ Isolation par école
- ✅ Recherche et filtrage
- ✅ Permissions

## Interface utilisateur

### Liste des élèves
- Tableau paginé 15/page
- Filtres: classe, statut, genre
- Recherche: nom, numéro, email
- Tri: nom, moyenne, date
- Actions rapides: Voir, Modifier, Supprimer
- Boutons: Ajouter, Statistiques, Exporter CSV

### Détail d'un élève
- Photo de profil
- Informations personnelles
- Adresse complète
- Contact parent
- Informations académiques
- Dates (création, modification)
- Actions: Modifier, Supprimer, Retour

### Formulaire d'ajout/modification
- 6 sections organisées
- Validation côté client et serveur
- Affichage d'erreurs
- Aide contextuelle
- Photo avec aperçu
- Boutons: Enregistrer, Annuler

### Statistiques
- Total élèves par statut
- Moyennes (globale et par classe)
- Répartition par classe (graphiques)
- Statistiques par genre
- Progression scolaire

## Dépannage

### Erreur: "student.school_id may be NULL"

```bash
python manage.py makemigrations
python manage.py migrate
```

### Pas d'élèves visibles

Vérifier que l'utilisateur a une école assignée:
```python
# Dans Django shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='director')
print(user.school)  # Ne doit pas être None
```

### "Permission denied" sur les actions

Vérifier le rôle:
```python
print(user.role)  # Doit être 'director' ou 'superadmin'
```

## Performance

- ✅ Indexation sur (school, grade) et (school, status)
- ✅ Requêtes optimisées
- ✅ Pagination au-dessus de 15 élèves
- ✅ Select_related/prefetch_related placés

Optimisation future:
- [ ] Recherche full-text avec PostgreSQL
- [ ] Cache redis
- [ ] Queryset dénormalisé

## Évolutions futures

```
- [ ] Import CSV d'élèves
- [ ] Générateur de cartes d'ID
- [ ] Absence/assiduité
- [ ] Notes et devoirs
- [ ] Communications parent-école
- [ ] Génération de certificats
- [ ] Rapports personnalisés
- [ ] API REST avec DRF
- [ ] Mobile app
```

## Support

Pour plus d'aide:
- Voir [STUDENTS_APP.md](STUDENTS_APP.md) pour la documentation complète
- Consulter les tests dans [apps/students/tests.py](apps/students/tests.py)
- Vérifier les templates dans [templates/students/](templates/students/)

---

**Créé le**: 19 Février 2026  
**Version**: 1.0  
**Statut**: Production-ready ✅
