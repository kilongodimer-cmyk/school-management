from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/', views.payments_list, name='payments_list'),
    path('students/<int:student_id>/payments/', views.student_payments, name='student_payments'),
    path('debtors/', views.debtor_list, name='debtor_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
