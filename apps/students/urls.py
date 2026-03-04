from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Liste des élèves
    path('', views.student_list, name='student_list'),
    
    # Détails d'un élève
    path('<int:pk>/', views.student_detail, name='student_detail'),
    
    # Créer un élève
    path('create/', views.student_create, name='student_create'),
    
    # Modifier un élève
    path('<int:pk>/edit/', views.student_edit, name='student_edit'),
    
    # Supprimer un élève
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Recherche AJAX
    path('search/', views.student_search, name='student_search'),
    
    # Exporter la liste
    path('export/', views.student_export_list, name='student_export'),
    
    # Actions en masse
    path('bulk-action/', views.student_bulk_action, name='student_bulk_action'),
    
    # Statistiques
    path('statistics/', views.student_statistics, name='student_statistics'),
]
