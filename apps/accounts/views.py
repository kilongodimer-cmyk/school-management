"""
Vues pour l'authentification et le système de rôles
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.db.models import Count, Q
from django.utils.decorators import method_decorator

from apps.accounts.models import CustomUser, School


# ============ DECORATEURS PERSONNALISÉS ============

def role_required(*roles):
    """
    Décorateur pour vérifier les rôles
    Usage: @role_required('director', 'teacher')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if request.user.role not in roles and not request.user.is_superuser:
                return redirect('permission_denied')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def school_owner_required(view_func):
    """
    Décorateur pour vérifier que l'utilisateur appartient à une école
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.school and not request.user.is_superuser:
            return redirect('permission_denied')
        
        return view_func(request, *args, **kwargs)
    return wrapper


# ============ MIXINS POUR CLASS-BASED VIEWS ============

class RoleRequiredMixin(LoginRequiredMixin):
    """Mixin pour vérifier les rôles dans les CBV"""
    required_roles = []
    login_url = 'accounts:login'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        
        if self.required_roles:
            user_role = getattr(request.user, 'role', None)
            if user_role not in self.required_roles and not request.user.is_superuser:
                return redirect('permission_denied')
        
        return super().dispatch(request, *args, **kwargs)


class SchoolOwnerMixin(LoginRequiredMixin):
    """Mixin pour vérifier que l'utilisateur appartient à une école"""
    login_url = 'accounts:login'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        
        user_school = getattr(request.user, 'school', None)
        if not user_school and not request.user.is_superuser:
            return redirect('permission_denied')
        
        return super().dispatch(request, *args, **kwargs)


class SchoolDataMixin:
    """Mixin pour filtrer les données par école"""
    
    def get_school(self):
        """Retourne l'école de l'utilisateur ou soulève une erreur"""
        if self.request.user.is_superuser:
            # Les superusers voient tout
            return None
        
        user_school = getattr(self.request.user, 'school', None)
        if not user_school:
            raise Http404("L'utilisateur n'appartient à aucune école")
        
        return user_school


# ============ VUES D'AUTHENTIFICATION ============

class LoginView(View):
    """Vue de connexion"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        """Afficher le formulaire de connexion"""
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        
        return render(request, self.template_name)
    
    def post(self, request):
        """Traiter la connexion"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Vérifier si le compte est actif et non suspendu
            if not user.is_active:
                context = {
                    'error': 'Votre compte a été désactivé.',
                    'username': username
                }
                return render(request, self.template_name, context)
            
            if user.is_banned:
                context = {
                    'error': 'Votre compte a été suspendu.',
                    'username': username
                }
                return render(request, self.template_name, context)
            
            # Connexion réussie
            login(request, user)
            
            # Redirection selon le rôle
            return redirect('accounts:dashboard')
        else:
            context = {
                'error': 'Nom d\'utilisateur ou mot de passe incorrect.',
                'username': username
            }
            return render(request, self.template_name, context)


class LogoutView(View):
    """Vue de déconnexion"""
    
    def get(self, request):
        """Déconnecter l'utilisateur"""
        logout(request)
        return redirect('accounts:login')


# ============ DASHBOARDS PAR RÔLE ============

@login_required(login_url='accounts:login')
def dashboard(request):
    """Dashboard principal avec redirection par rôle"""
    
    user_role = getattr(request.user, 'role', None)

    if request.user.is_superuser or user_role == 'superadmin':
        return redirect('accounts:admin_dashboard')
    
    elif user_role == 'director':
        return redirect('accounts:director_dashboard')
    
    elif user_role == 'teacher':
        return redirect('accounts:teacher_dashboard')
    
    elif user_role == 'accountant':
        return redirect('accounts:accountant_dashboard')
    
    elif user_role in ['student', 'parent']:
        return redirect('accounts:student_dashboard')
    
    # Par défaut
    return redirect('accounts:profile')


class AdminDashboardView(RoleRequiredMixin, TemplateView):
    """Dashboard pour les super admins"""
    template_name = 'accounts/dashboards/admin_dashboard.html'
    required_roles = ['superadmin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_schools'] = School.objects.count()
        context['total_users'] = CustomUser.objects.count()
        context['active_users'] = CustomUser.objects.filter(is_active=True).count()
        context['schools'] = School.objects.all()
        
        # Statistiques par rôle
        context['users_by_role'] = dict(
            CustomUser.objects.values('role').annotate(count=Count('id')).values_list('role', 'count')
        )
        
        return context


class DirectorDashboardView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Dashboard pour les directeurs"""
    template_name = 'accounts/dashboards/director_dashboard.html'
    required_roles = ['director']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        school = self.request.user.school
        context['school'] = school
        
        # Statistiques de l'école
        context['total_users'] = school.users.count()
        context['total_teachers'] = school.users.filter(role='teacher').count()
        context['total_students'] = school.users.filter(role='student').count()
        context['total_parents'] = school.users.filter(role='parent').count()
        context['total_accountants'] = school.users.filter(role='accountant').count()
        
        # Utilisateurs actifs et vérifiés
        context['active_users'] = school.users.filter(is_active=True).count()
        context['verified_users'] = school.users.filter(is_verified=True).count()
        
        # Listes
        context['teachers'] = school.users.filter(role='teacher')[:10]
        context['recent_users'] = school.users.order_by('-created_at')[:10]
        
        return context


class TeacherDashboardView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Dashboard pour les enseignants"""
    template_name = 'accounts/dashboards/teacher_dashboard.html'
    required_roles = ['teacher']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        teacher = self.request.user
        school = teacher.school
        
        context['school'] = school
        context['teacher'] = teacher
        
        # Statistiques
        context['total_students'] = school.users.filter(role='student').count()
        context['total_classes'] = 0  # À implémenter avec les cours
        context['pending_grades'] = 0  # À implémenter avec les notes
        
        return context


class StudentDashboardView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Dashboard pour les étudiants et parents"""
    template_name = 'accounts/dashboards/student_dashboard.html'
    required_roles = ['student', 'parent']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        school = user.school
        
        context['school'] = school
        context['user'] = user
        
        # Statistiques
        if user.role == 'student':
            context['message'] = 'Bienvenue sur votre tableau de bord étudiant'
        else:
            context['message'] = 'Bienvenue sur votre tableau de bord parent'
        
        return context


class AccountantDashboardView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Dashboard pour les comptables"""
    template_name = 'accounts/dashboards/accountant_dashboard.html'
    required_roles = ['accountant']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        accountant = self.request.user
        school = accountant.school
        
        context['school'] = school
        context['accountant'] = accountant
        
        # Statistiques financières
        context['total_users'] = school.users.count()
        
        return context


# ============ PROFIL ET PARAMÈTRES ============

@login_required(login_url='accounts:login')
def profile_view(request):
    """Afficher et modifier le profil utilisateur"""
    user = request.user
    
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
        
        # Gérer l'upload de photo
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        
        user.save()
        
        return redirect('accounts:profile')
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def change_password(request):
    """Changer le mot de passe"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Vérifier l'ancien mot de passe
        if not request.user.check_password(old_password):
            context = {
                'error': 'L\'ancien mot de passe est incorrect.',
            }
            return render(request, 'accounts/change_password.html', context)
        
        # Vérifier que les nouveaux mots de passe correspondent
        if new_password != confirm_password:
            context = {
                'error': 'Les nouveaux mots de passe ne correspondent pas.',
            }
            return render(request, 'accounts/change_password.html', context)
        
        # Changer le mot de passe
        request.user.set_password(new_password)
        request.user.save()
        
        # Reconnecter l'utilisateur
        login(request, request.user)
        
        context = {
            'success': 'Votre mot de passe a été changé avec succès.',
        }
        return render(request, 'accounts/change_password.html', context)
    
    return render(request, 'accounts/change_password.html')


# ============ GESTION DES UTILISATEURS ============

class UserListView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Liste des utilisateurs (filtrée par école)"""
    template_name = 'accounts/users/user_list.html'
    required_roles = ['director', 'superadmin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        school = self.request.user.school
        
        # Filtrer par rôle si demandé
        role = self.request.GET.get('role')
        if role:
            users = school.users.filter(role=role)
        else:
            users = school.users.all()
        
        # Filtrer par statut
        status = self.request.GET.get('status')
        if status == 'active':
            users = users.filter(is_active=True)
        elif status == 'inactive':
            users = users.filter(is_active=False)
        elif status == 'banned':
            users = users.filter(is_banned=True)
        
        context['users'] = users
        context['roles'] = CustomUser.ROLE_CHOICES
        
        return context


class UserDetailView(RoleRequiredMixin, SchoolDataMixin, TemplateView):
    """Détail d'un utilisateur"""
    template_name = 'accounts/users/user_detail.html'
    required_roles = ['director', 'superadmin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_id = kwargs.get('user_id')
        school = self.request.user.school
        
        # Vérifier que l'utilisateur appartient à la même école
        try:
            user = school.users.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404("Utilisateur non trouvé")
        
        context['profile_user'] = user
        
        return context


# ============ GESTION DES ÉCOLES ============

@role_required('superadmin')
def school_list(request):
    """Liste de toutes les écoles (superadmin seulement)"""
    schools = School.objects.all()
    
    # Filtrer par statut
    is_active = request.GET.get('active')
    if is_active:
        schools = schools.filter(is_active=is_active == 'true')
    
    context = {
        'schools': schools,
    }
    return render(request, 'accounts/schools/school_list.html', context)


@role_required('superadmin')
def school_detail(request, school_id):
    """Détail d'une école"""
    school = School.objects.get(id=school_id)
    
    context = {
        'school': school,
        'total_users': school.users.count(),
        'users_by_role': dict(
            school.users.values('role').annotate(count=Count('id')).values_list('role', 'count')
        ),
    }
    return render(request, 'accounts/schools/school_detail.html', context)


# ============ PERMISSION DENIED ============

def permission_denied(request):
    """Page d'erreur de permission"""
    return render(request, 'accounts/permission_denied.html', status=403)
