"""
URLs de l'application accounts
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ========== AUTHENTIFICATION ==========
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # ========== DASHBOARDS ==========
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('director-dashboard/', views.DirectorDashboardView.as_view(), name='director_dashboard'),
    path('teacher-dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student-dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('accountant-dashboard/', views.AccountantDashboardView.as_view(), name='accountant_dashboard'),
    
    # ========== PROFIL ==========
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # ========== GESTION DES UTILISATEURS ==========
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # ========== GESTION DES ÉCOLES ==========
    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:school_id>/', views.school_detail, name='school_detail'),
    
    # ========== ERREURS ==========
    path('permission-denied/', views.permission_denied, name='permission_denied'),
]
