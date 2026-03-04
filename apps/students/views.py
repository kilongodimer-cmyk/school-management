from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from apps.accounts.models import School
from .models import Student
from .forms import StudentForm, StudentSearchForm, BulkStudentActionForm, StudentFilterForm


# =====================================================
# Mixins for protection
# =====================================================

class SchoolDataMixin:
    """
    Mixin pour filtrer les données par l'école de l'utilisateur
    S'assure que chaque utilisateur ne voit que les élèves de son école
    """
    
    def get_queryset(self):
        """Filtrer par l'école de l'utilisateur"""
        queryset = super().get_queryset()
        
        # Super admin voit tous les élèves
        if self.request.user.is_superuser or self.request.user.role == 'superadmin':
            return queryset
        
        # Autres utilisateurs voient uniquement les élèves de leur école
        if self.request.user.school:
            return queryset.filter(school=self.request.user.school)
        
        return queryset.none()


class StudentDirectorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin pour restreindre l'accès aux directeurs et super admin
    """
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['superadmin', 'director']
    
    def handle_no_permission(self):
        messages.error(self.request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('accounts:dashboard')


# =====================================================
# Function-based Views
# =====================================================

@login_required
def student_list(request):
    """
    Afficher la liste des élèves avec recherche et filtrage
    """
    # Déterminer le queryset en fonction du rôle
    if request.user.is_superuser or request.user.role == 'superadmin':
        students = Student.objects.all()
    else:
        if request.user.school:
            students = request.user.school.students.all()
        else:
            students = Student.objects.none()
    
    # Filtre de recherche
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filtrer par classe
    grade_filter = request.GET.get('grade', '')
    if grade_filter:
        students = students.filter(grade__icontains=grade_filter)
    
    # Filtrer par statut
    status_filter = request.GET.get('status', '')
    if status_filter:
        students = students.filter(status=status_filter)
    
    # Filtrer par genre
    gender_filter = request.GET.get('gender', '')
    if gender_filter:
        students = students.filter(gender=gender_filter)
    
    # Tri
    sort_by = request.GET.get('sort_by', 'last_name')
    if sort_by:
        students = students.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(students, 15)  # 15 élèves par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'students': page_obj.object_list,
        'total_count': paginator.count,
        'search_form': StudentSearchForm(request.GET),
        'search_query': search_query,
        'grade_filter': grade_filter,
    }
    
    return render(request, 'students/student_list.html', context)


@login_required
def student_detail(request, pk):
    """
    Afficher les détails d'un élève
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Vérification de l'accès
    if not request.user.is_superuser and request.user.role != 'superadmin':
        if request.user.school != student.school:
            messages.error(request, 'Vous n\'avez pas accès à cet élève.')
            return redirect('students:student_list')
    
    context = {
        'student': student,
        'age': student.age,
    }
    
    return render(request, 'students/student_detail.html', context)


@login_required
def student_create(request):
    """
    Créer un nouvel élève
    """
    # Vérification des permissions
    if not request.user.is_superuser and request.user.role not in ['superadmin', 'director']:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('students:student_list')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            
            # Assigner l'école de l'utilisateur si pas super admin
            if not request.user.is_superuser and request.user.role != 'superadmin':
                if request.user.school:
                    student.school = request.user.school
            
            student.save()
            messages.success(request, f'L\'élève {student.full_name} a été créé avec succès.')
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Créer un nouvel élève',
    }
    
    return render(request, 'students/student_form.html', context)


@login_required
def student_edit(request, pk):
    """
    Modifier un élève
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Vérification des permissions
    if not request.user.is_superuser and request.user.role not in ['superadmin', 'director']:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('students:student_list')
    
    if not request.user.is_superuser and request.user.role != 'superadmin':
        if request.user.school != student.school:
            messages.error(request, 'Vous ne pouvez modifier que les élèves de votre école.')
            return redirect('students:student_list')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'L\'élève {student.full_name} a été modifié avec succès.')
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Modifier {student.full_name}',
    }
    
    return render(request, 'students/student_form.html', context)


@login_required
def student_delete(request, pk):
    """
    Supprimer un élève
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Vérification des permissions
    if not request.user.is_superuser and request.user.role not in ['superadmin', 'director']:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('students:student_list')
    
    if not request.user.is_superuser and request.user.role != 'superadmin':
        if request.user.school != student.school:
            messages.error(request, 'Vous ne pouvez supprimer que les élèves de votre école.')
            return redirect('students:student_list')
    
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f'L\'élève {student_name} a été supprimé avec succès.')
        return redirect('students:student_list')
    
    context = {
        'student': student,
    }
    
    return render(request, 'students/student_confirm_delete.html', context)


@login_required
def student_search(request):
    """
    Endpoint pour la recherche AJAX d'élèves
    """
    query = request.GET.get('q', '')
    
    # Récupérer les élèves de l'école de l'utilisateur
    if request.user.is_superuser or request.user.role == 'superadmin':
        students = Student.objects.all()
    else:
        if request.user.school:
            students = request.user.school.students.all()
        else:
            students = Student.objects.none()
    
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query)
        )[:10]  # Limiter à 10 résultats
    
    results = [
        {
            'id': student.id,
            'text': f'{student.full_name} ({student.student_id})',
        }
        for student in students
    ]
    
    return JsonResponse({'results': results})


@login_required
def student_export_list(request):
    """
    Exporter la liste des élèves en CSV
    """
    import csv
    from django.http import HttpResponse
    
    # Récupérer les élèves de l'école
    if request.user.is_superuser or request.user.role == 'superadmin':
        students = Student.objects.all()
    else:
        if request.user.school:
            students = request.user.school.students.all()
        else:
            students = Student.objects.none()
    
    # Créer la réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="eleves.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Numéro',
        'Prénom',
        'Nom',
        'Classe',
        'Genre',
        'Email',
        'Téléphone',
        'Moyenne',
        'Parent',
        'Téléphone parent',
        'Statut',
        'Date inscription',
    ])
    
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.grade,
            student.get_gender_display(),
            student.email or '',
            student.phone or '',
            student.gpa or '',
            student.parent_name or '',
            student.parent_phone or '',
            student.get_status_display(),
            student.created_at.strftime('%d/%m/%Y'),
        ])
    
    return response


@login_required
def student_bulk_action(request):
    """
    Effectuer des actions en masse sur les élèves
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        student_ids = request.POST.getlist('students')
        
        if not student_ids:
            messages.warning(request, 'Veuillez sélectionner au moins un élève.')
            return redirect('students:student_list')
        
        # Récupérer les élèves de l'école de l'utilisateur
        if request.user.is_superuser or request.user.role == 'superadmin':
            students = Student.objects.filter(id__in=student_ids)
        else:
            if request.user.school:
                students = request.user.school.students.filter(id__in=student_ids)
            else:
                students = Student.objects.none()
        
        if action == 'activate':
            students.update(status='active')
            messages.success(request, f'{students.count()} élève(s) activé(s).')
        elif action == 'deactivate':
            students.update(status='inactive')
            messages.success(request, f'{students.count()} élève(s) désactivé(s).')
        elif action == 'graduate':
            students.update(status='graduated')
            messages.success(request, f'{students.count()} élève(s) diplômé(s).')
        elif action == 'suspend':
            students.update(status='suspended')
            messages.success(request, f'{students.count()} élève(s) suspendu(s).')
    
    return redirect('students:student_list')


@login_required
def student_statistics(request):
    """
    Afficher les statistiques des élèves
    """
    # Récupérer les élèves
    if request.user.is_superuser or request.user.role == 'superadmin':
        students = Student.objects.all()
    else:
        if request.user.school:
            students = request.user.school.students.all()
        else:
            students = Student.objects.none()
    
    total_students = students.count()
    active_students = students.filter(status='active').count()
    inactive_students = students.filter(status='inactive').count()
    graduated_students = students.filter(status='graduated').count()
    suspended_students = students.filter(status='suspended').count()
    
    # Statistiques par classe
    grade_stats = []
    grades = students.values('grade').distinct()
    for grade_obj in grades:
        grade = grade_obj['grade']
        count = students.filter(grade=grade).count()
        grade_stats.append({'grade': grade, 'count': count})
    
    # Moyenne générale
    avg_gpa = students.filter(gpa__isnull=False).values('gpa')
    if avg_gpa:
        from django.db.models import Avg
        avg_gpa = students.aggregate(Avg('gpa'))['gpa__avg']
    else:
        avg_gpa = None
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'graduated_students': graduated_students,
        'suspended_students': suspended_students,
        'grade_stats': grade_stats,
        'avg_gpa': avg_gpa,
    }
    
    return render(request, 'students/student_statistics.html', context)
