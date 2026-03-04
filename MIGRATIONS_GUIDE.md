# 🗂️ MIGRATIONS - GUIDE COMPLET

## Qu'est-ce qu'une migration ?

Une migration Django est un fichier Python qui décrit les modifications à apporter à la base de données. Elle permet de :
- Versionner le schéma de la base de données
- Reproduire les modifications sur d'autres environnements
- Revenir à une version antérieure si nécessaire

## Commandes principales

### 1. Créer les migrations
```bash
python manage.py makemigrations
```

**Résultat attendu :**
```
Migrations for 'accounts':
  apps/accounts/migrations/0001_initial.py
    - Create model School
    - Create model CustomUser
```

Cette commande analyse vos modèles et crée les fichiers de migration correspondants.

### 2. Afficher l'état des migrations
```bash
python manage.py showmigrations
```

**Résultat attendu :**
```
accounts
 [ ] 0001_initial
 [ ] 0002_customuser_bio
...
```
- `[ ]` = Migration non appliquée
- `[X]` = Migration appliquée

### 3. Appliquer les migrations
```bash
python manage.py migrate
```

**Résultat attendu :**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions
Running migrations:
  Applying accounts.0001_initial... OK
```

### 4. Appliquer les migrations d'une app spécifique
```bash
python manage.py migrate accounts
```

### 5. Revenir à une migration antérieure
```bash
python manage.py migrate accounts 0001
```

### 6. Afficher le SQL généré
```bash
python manage.py sqlmigrate accounts 0001
```

## Structure d'une migration

```python
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(...)),
                ('name', models.CharField(max_length=255, unique=True)),
                # ... autres champs
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                # ... champs
                ('school', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='accounts.school',
                )),
            ],
        ),
    ]
```

## Workflow complet pour l'app accounts

### Étape 1 : Première configuration
```bash
# 1. Vérifier que settings.py a AUTH_USER_MODEL = 'accounts.CustomUser'
# 2. Vérifier que 'apps.accounts' est dans INSTALLED_APPS

# 3. Créer les migrations initiales
python manage.py makemigrations

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superutilisateur
python manage.py createsuperuser
```

### Étape 2 : Ajouter un champ au modèle
```python
# Dans models.py, ajouter un champ à CustomUser
class CustomUser(AbstractUser):
    # ... champs existants ...
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
```

Puis :
```bash
# Créer la migration
python manage.py makemigrations

# Appliquer la migration
python manage.py migrate
```

### Étape 3 : Modifier un champ existant
```python
# Changer un champ
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500)  # Avant : max_length=100
```

Puis :
```bash
python manage.py makemigrations
python manage.py migrate
```

## Bonnes pratiques

### ✅ À faire

1. **Toujours créer des migrations explicites**
```bash
python manage.py makemigrations --name add_user_bio
```

2. **Vérifier les migrations avant de les appliquer**
```bash
python manage.py sqlmigrate accounts 0001
```

3. **Tester les migrations en développement avant production**
```bash
# Test sur une copie de la base de production
python manage.py migrate --settings=settings_test
```

4. **Utiliser des noms explicites**
```
0001_initial.py        ✓ Bon
0002_add_user_bio.py   ✓ Bon
0003_alter_school_name.py  ✓ Bon
```

5. **Commiter les migrations dans Git**
```bash
git add apps/accounts/migrations/
git commit -m "Add user bio field to CustomUser"
```

### ❌ À éviter

1. **Ne pas modifier les migrations appliquées**
   - Si c'est déjà appliqué, créer une nouvelle migration
   
2. **Ne pas supprimer les migrations** (sauf en développement local)
   - Les supprimer peut causer des problèmes de synchronisation
   
3. **Ne pas utiliser `--fake` sans bien comprendre**
   - `--fake` marque une migration comme appliquée sans la lancer
   - À utiliser seulement en cas de problème connu
   
4. **Ne pas mettre à jour les migrations existantes**
   - Créer une nouvelle migration à la place

## Problèmes courants et solutions

### Problème 1 : "django.core.management.base.SystemCheckError: SystemCheckError: System check identified some issues"

**Cause** : Le modèle CustomUser n'est pas configuré comme AUTH_USER_MODEL

**Solution** :
```python
# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Problème 2 : "No changes detected in app 'accounts'"

**Cause** : Les modèles n'ont pas changé, ou Django ne les détecte pas

**Solution** :
```bash
# Vérifier que les modèles sont correctement définis
python manage.py makemigrations --dry-run --verbosity 3
```

### Problème 3 : Migration appliquée pas complètement

**Cause** : Erreur pendant l'application d'une migration

**Solution** :
```bash
# Revenir à la migration précédente
python manage.py migrate accounts 0001

# Vérifier l'état
python manage.py showmigrations accounts

# Appliquer de nouveau
python manage.py migrate
```

### Problème 4 : "Relation "accounts_customuser" does not exist"

**Cause** : Les migrations n'ont pas été appliquées correctement

**Solution** :
```bash
# Vérifier l'état
python manage.py showmigrations

# Appliquer les migrations manquantes
python manage.py migrate
```

## Opérations de migration avancées

### Ajouter un champ avec une valeur par défaut

```python
# models.py
class CustomUser(AbstractUser):
    age = models.IntegerField(default=18)  # Nouvelle valeur par défaut
```

Django demande comment remplir les lignes existantes :
```
? Select an option: 
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit and manually define a default
```

### Renommer un champ

```bash
# Créer une migration vide
python manage.py makemigrations --empty accounts --name rename_field

# Éditer la migration
# Utiliser operations.RenameField(...)
```

### Supprimer un champ

```python
# Simplement retirer le champ du modèle
class CustomUser(AbstractUser):
    # bio supprimé
    pass
```

Puis :
```bash
python manage.py makemigrations
python manage.py migrate
```

### Supprimer une table

```python
# Supprimer le modèle du fichier models.py
# ou décommenter simplement
```

Puis :
```bash
python manage.py makemigrations
python manage.py migrate
```

## Vérification après migration

```bash
# 1. Vérifier que tout est OK
python manage.py check

# 2. Afficher l'état
python manage.py showmigrations

# 3. Vérifier la structure de la base
python manage.py dbshell
\d accounts_customuser  # PostgreSQL
desc accounts_customuser;  # MySQL
.schema accounts_customuser  # SQLite
```

## Pour aller plus loin

- [Documentation Django Migrations](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [Exemples de migrations avancées](https://docs.djangoproject.com/en/4.2/howto/writing-migrations/)
- [Opérations de migration](https://docs.djangoproject.com/en/4.2/ref/migration-operations/)

---

**Les migrations sont maintenant configurées pour l'app accounts !** ✅
