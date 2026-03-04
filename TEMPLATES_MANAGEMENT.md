# Templates de Gestion - Documentation

## Vue d'ensemble
Ces templates complètent le système d'authentification en fournissant des interfaces pour la gestion des utilisateurs et des écoles.

## Templates créés

### 1. **user_list.html** - Liste des utilisateurs
**Chemin:** `templates/accounts/users/user_list.html`

**Fonctionnalités:**
- Filtrage par rôle (tous les rôles disponibles)
- Filtrage par statut (Actif, Inactif, Suspendu)
- Tableau responsif avec colonnes:
  - Nom (avec lien vers le profil)
  - Email
  - Rôle (avec badge de couleur)
  - Statut (Actif/Inactif/Suspendu)
  - Vérification (Vérifié/En attente)
  - Date de création
  - Lien vers les détails
- Bouton pour ajouter un nouvel utilisateur
- Affichage d'un message si aucun utilisateur trouvé

**Accessibilité:** Directeurs pour leurs écoles, Super Admin pour toutes les écoles

---

### 2. **user_detail.html** - Détails d'un utilisateur
**Chemin:** `templates/accounts/users/user_detail.html`

**Sections:**
1. **Photo de profil**
   - Avatar ou placeholder
   - Rôle avec badge
   - Statut et vérification

2. **Informations personnelles**
   - Prénom, Nom
   - Email, Nom d'utilisateur
   - Téléphone, Biographie

3. **Adresse**
   - Adresse complète
   - Ville, Code postal, Pays

4. **École**
   - Lien vers l'école
   - Code, Localisation

5. **Dates**
   - Date d'inscription
   - Dernière connexion

**Modals inclus:**
1. **Modifier l'utilisateur**
   - Changer le rôle
   - Marquer comme vérifié
   
2. **Réinitialiser le mot de passe**
   - Sécurité: validation du mot de passe admin
   - Génère un MDP temporaire à envoyer

**Actions:**
- Modifier (Modal)
- Suspendre/Réactiver
- Réinitialiser le mot de passe
- Retour à la liste

---

### 3. **school_list.html** - Liste des écoles
**Chemin:** `templates/accounts/schools/school_list.html`

**Fonctionnalités:**
- Recherche par nom ou code d'école
- Filtrage par statut (Actives, Inactives)
- **Statistiques globales:**
  - Nombre d'écoles totales
  - Écoles actives
  - Utilisateurs totaux
  - Capacité totale combinée

- **Tableau avec colonnes:**
  - Nom
  - Code
  - Localisation (Ville, Pays)
  - Directeur
  - Nombre d'utilisateurs (badge)
  - Capacité (étudiants et enseignants)
  - Statut
  - Date de création
  - Lien vers les détails

**Accessibilité:** Super Admin uniquement

---

### 4. **school_detail.html** - Détails d'une école
**Chemin:** `templates/accounts/schools/school_detail.html`

**Sections:**
1. **Informations générales**
   - Nom, Code
   - Email, Téléphone
   - Site web
   - Statut
   - Logo

2. **Localisation**
   - Adresse complète
   - Ville, Code postal
   - Pays

3. **Capacité**
   - Barres de progression pour étudiants
   - Barres de progression pour enseignants
   - Pourcentage de capacité utilisée

4. **Utilisateurs par rôle**
   - Compte des enseignants
   - Compte des étudiants
   - Compte des parents
   - Compte des comptables
   - Affichage en cartes colorées

5. **Directeur**
   - Photo, Nom, Email
   - Téléphone, Adresse
   - Lien vers le profil complet

6. **Dates**
   - Création
   - Dernière modification

**Modals inclus:**
1. **Modifier l'école**
   - Nom, Code
   - Email, Téléphone
   - Capacités (étudiants, enseignants)

**Actions:**
- Modifier (Modal)
- Activer/Désactiver
- Voir les utilisateurs

---

## Styles Bootstrap 5 appliqués

### Classes personnalisées:
- `.badge-role` - Badges de rôles avec couleurs
- `.badge-teacher` - Vert (enseignant)
- `.badge-student` - Bleu (étudiant)
- `.badge-director` - Bleu foncé (directeur)
- `.badge-accountant` - Orange (comptable)
- `.badge-parent` - Rose (parent)
- `.badge-superadmin` - Rouge (super admin)

### Composants:
- Tables responsives avec hover effects
- Cartes de statistiques avec icons
- Barres de progression Bootstrap
- Modals pour les actions critiques
- Alerts pour les messages et états
- Forms avec validation

---

## Intégration avec le système existant

### URLs correspondantes (à configurer dans urls.py):
```python
# Users
path('users/', views.UserListView.as_view(), name='user_list'),
path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

# Schools
path('schools/', views.school_list, name='school_list'),
path('schools/<int:pk>/', views.school_detail, name='school_detail'),
```

### Contextes à fournir:

**user_list:**
- `users` - Queryset des utilisateurs
- `roles` - Liste des rôles disponibles

**user_detail:**
- `user` - Instance CustomUser
- `roles` - Liste des rôles

**school_list:**
- `schools` - Queryset des écoles
- `total_schools` - Nombre total
- `active_schools` - Écoles actives
- `total_users` - Nombre d'utilisateurs
- `total_capacity` - Capacité totale

**school_detail:**
- `school` - Instance School
- `director` - Directeur de l'école
- `teachers_count` - Nombre d'enseignants
- `students_count` - Nombre d'étudiants
- `parents_count` - Nombre de parents
- `accountants_count` - Nombre de comptables
- `current_students` - Étudiants inscrits
- `current_teachers` - Enseignants inscrits

---

## Fonctionnalités avancées à implémenter

1. **Pagination** - Ajouter django.core.paginator.Paginator
2. **Tri** - Liens pour trier par colonne
3. **Recherche en temps réel** - AJAX
4. **Export** - Exporter en PDF/CSV
5. **Bulk actions** - Sélection multiple d'utilisateurs
6. **Historique** - Logs des modifications

---

## Checkliste d'implémentation

- [ ] Créer/mettre à jour les vues pour fournir les contextes corrects
- [ ] Ajouter les URLs correspondantes
- [ ] Tester les filtres
- [ ] Tester les modals
- [ ] Ajouter les permissions pour l'accès
- [ ] Tester la responsivité mobile
- [ ] Ajouter les messages flash après actions
- [ ] Implémenter les actions des boutons (Modifier, Suspendre, etc.)
- [ ] Ajouter la paginatio si nécessaire
- [ ] Tester avec différents rôles

