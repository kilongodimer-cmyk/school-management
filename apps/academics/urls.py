from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Classes URLs
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/<int:pk>/edit/', views.class_update, name='class_update'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),
    
    # Subjects URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subjects/<int:pk>/edit/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    
    # Class Subjects URLs (linking subjects to classes)
    path('classes/<int:class_pk>/subjects/add/', views.class_subject_create, name='class_subject_create'),
    path('classes/<int:class_pk>/subjects/<int:subject_pk>/edit/', views.class_subject_update, name='class_subject_update'),
    path('classes/<int:class_pk>/subjects/<int:subject_pk>/delete/', views.class_subject_delete, name='class_subject_delete'),
    
    # Grades URLs
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/create/', views.grade_create, name='grade_create'),
    path('grades/<int:pk>/edit/', views.grade_update, name='grade_update'),
    path('grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),
    
    # Results URLs
    path('students/<int:pk>/results/', views.student_results, name='student_results'),
    path('students/<int:pk>/report_pdf/', views.generate_report_card_pdf, name='student_report_pdf'),
    path('classes/<int:class_pk>/results/', views.class_results, name='class_results'),
]
