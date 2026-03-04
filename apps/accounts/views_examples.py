"""
Exemples d'utilisation de l'app accounts dans les vues
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from apps.accounts.models import School, CustomUser


# ============ EXEMPLES DE VUES BASIQUES ============

@login_required
def user_profile(request):
    """Affiche le profil de l'utilisateur connecté"""
    user = request.user
    context = {
        'user': user,
        'school': user.school,
        'role': user.get_role_display(),
        'is_verified': user.is_verified,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def school_dashboard(request):
    """Tableau de bord d'une école"""
    if not request.user.school:
        return redirect('home')
    
    school = request.user.school
    context = {
        'school': school,
        'total_users': school.users.count(),
        'teachers': school.users.filter(role='teacher').count(),
        'students': school.users.filter(role='student').count(),
        'parents': school.users.filter(role='parent').count(),
    }
    return render(request, 'accounts/school_dashboard.html', context)


# ============ EXEMPLES DE VÉRIFICATION DE RÔLES ============

@login_required
def teacher_only_view(request):
    """Vue accessible uniquement aux enseignants"""
    if not request.user.is_teacher():
        return redirect('permission_denied')
    
    # Logique pour les enseignants
    school = request.user.school
    context = {
        'teacher': request.user,
        'school': school,
    }
    return render(request, 'accounts/teacher_view.html', context)


@login_required
def director_only_view(request):
    """Vue accessible uniquement aux directeurs"""
    if not request.user.is_director():
        return redirect('permission_denied')
    
    school = request.user.school
    context = {
        'director': request.user,
        'school': school,
        'staff': school.users.exclude(role='student', role='parent'),
    }
    return render(request, 'accounts/director_view.html', context)


@login_required
def admin_only_view(request):
    """Vue accessible uniquement aux superadmins"""
    if not request.user.is_superadmin():
        return redirect('permission_denied')
    
    context = {
        'schools': School.objects.all(),
        'total_schools': School.objects.count(),
        'total_users': CustomUser.objects.count(),
    }
    return render(request, 'accounts/admin_view.html', context)


# ============ EXEMPLES DE REQUÊTES AUX MODÈLES ============

@login_required
def list_school_users(request):
    """Liste tous les utilisateurs d'une école"""
    if not request.user.school:
        return JsonResponse({'error': 'L\'utilisateur n\'appartient à aucune école'})
    
    school = request.user.school
    
    # Récupérer tous les utilisateurs de l'école
    users = school.users.all()
    
    # Filtrer par rôle si demandé
    role = request.GET.get('role')
    if role:
        users = users.filter(role=role)
    
    # Préparer les données
    data = {
        'school': school.name,
        'users': [
            {
                'id': user.id,
                'name': user.get_full_name(),
                'email': user.email,
                'role': user.get_role_display(),
                'is_verified': user.is_verified,
            }
            for user in users
        ]
    }
    return JsonResponse(data)


@login_required
def list_teachers(request):
    """Liste tous les enseignants"""
    if not request.user.is_superadmin() and not request.user.is_director():
        return redirect('permission_denied')
    
    school = request.user.school or School.objects.all()
    
    # Requête optimisée avec select_related
    teachers = CustomUser.objects.select_related('school').filter(
        school=school,
        role='teacher',
        is_active=True
    )
    
    context = {
        'teachers': teachers,
    }
    return render(request, 'accounts/teachers_list.html', context)


@login_required
def user_detail(request, user_id):
    """Détail d'un utilisateur"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Vérifier les permissions
    if not request.user.is_superadmin():
        if request.user != user and request.user.school != user.school:
            return redirect('permission_denied')
    
    context = {
        'profile_user': user,
        'school': user.school,
    }
    return render(request, 'accounts/user_detail.html', context)


# ============ EXEMPLES D'OPÉRATIONS CRUD ============

@login_required
def create_user(request):
    """Créer un nouvel utilisateur (directeur seulement)"""
    if not request.user.is_director():
        return redirect('permission_denied')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        password = request.POST.get('password')
        
        # Créer l'utilisateur
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            school=request.user.school,
            role=role,
            is_verified=True,  # Directeur crée des comptes vérifiés
        )
        
        return redirect('accounts:user_detail', user_id=user.id)
    
    context = {
        'roles': CustomUser.ROLE_CHOICES,
    }
    return render(request, 'accounts/create_user.html', context)


@login_required
def update_user(request, user_id):
    """Mettre à jour un utilisateur"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Vérifier les permissions
    if request.user != user and not request.user.is_superadmin():
        return redirect('permission_denied')
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.country = request.POST.get('country', user.country)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.bio = request.POST.get('bio', user.bio)
        user.save()
        
        return redirect('accounts:user_detail', user_id=user.id)
    
    context = {
        'profile_user': user,
    }
    return render(request, 'accounts/update_user.html', context)


@login_required
def delete_user(request, user_id):
    """Supprimer un utilisateur (superadmin seulement)"""
    if not request.user.is_superadmin():
        return redirect('permission_denied')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:user_list')
    
    context = {
        'profile_user': user,
    }
    return render(request, 'accounts/confirm_delete.html', context)


# ============ EXEMPLES DE REQUÊTES FILTRÉES ============

def school_list(request):
    """Liste des écoles avec filtrage"""
    schools = School.objects.all()
    
    # Filtrer par statut
    is_active = request.GET.get('active')
    if is_active:
        schools = schools.filter(is_active=is_active == 'true')
    
    # Filtrer par pays
    country = request.GET.get('country')
    if country:
        schools = schools.filter(country=country)
    
    # Filtrer par ville
    city = request.GET.get('city')
    if city:
        schools = schools.filter(city=city)
    
    # Requête optimisée avec prefetch_related
    schools = schools.prefetch_related('users')
    
    context = {
        'schools': schools,
    }
    return render(request, 'accounts/school_list.html', context)


# ============ EXEMPLES AVEC CLASS-BASED VIEWS ============

class SchoolListView(ListView):
    """Liste toutes les écoles"""
    model = School
    template_name = 'accounts/school_list_cbv.html'
    context_object_name = 'schools'
    paginate_by = 10
    
    def get_queryset(self):
        """Requête optimisée"""
        return School.objects.all().prefetch_related('users')


class SchoolDetailView(DetailView):
    """Détail d'une école"""
    model = School
    template_name = 'accounts/school_detail.html'
    context_object_name = 'school'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.get_object()
        context['teachers'] = school.users.filter(role='teacher')
        context['students'] = school.users.filter(role='student')
        context['staff'] = school.users.exclude(role__in=['student', 'parent'])
        return context


class UserListView(ListView):
    """Liste les utilisateurs avec filtrage"""
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        """Requête avec filtrage"""
        queryset = CustomUser.objects.select_related('school')
        
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        school = self.request.GET.get('school')
        if school:
            queryset = queryset.filter(school_id=school)
        
        return queryset


# ============ EXEMPLES POUR L'API ============

@login_required
def api_school_users(request, school_id):
    """API pour récupérer les utilisateurs d'une école"""
    school = get_object_or_404(School, id=school_id)
    
    # Vérifier les permissions
    if not request.user.is_superadmin() and request.user.school != school:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    users = school.users.values('id', 'username', 'email', 'first_name', 'last_name', 'role')
    return JsonResponse(list(users), safe=False)


@login_required
def api_user_stats(request):
    """API pour les statistiques utilisateurs"""
    if not request.user.is_superadmin():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_schools': School.objects.count(),
        'users_by_role': dict(
            CustomUser.objects.values('role').annotate(
                count=Count('id')
            ).values_list('role', 'count')
        ),
        'active_users': CustomUser.objects.filter(is_active=True).count(),
        'verified_users': CustomUser.objects.filter(is_verified=True).count(),
    }
    return JsonResponse(stats)
