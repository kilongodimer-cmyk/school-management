from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg, F, Case, When, Value, FloatField
from django.contrib import messages
from apps.accounts.models import School
from .models import Class, Subject, AcademicYear, ClassSubject, Term, Grade
from .forms import ClassForm, SubjectForm, AcademicYearForm, ClassSubjectForm, TermForm, GradeForm
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors


class SchoolDataMixin(UserPassesTestMixin):
    """Mixin pour assurer l'isolation par école"""
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'school'):
            queryset = queryset.filter(school=self.request.user.school)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school'] = self.request.user.school
        return context


# ==================== CLASSES VIEWS ====================

@login_required
def class_list(request):
    """List all classes for the school"""
    school = request.user.school
    classes = Class.objects.filter(school=school).select_related('academic_year')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        classes = classes.filter(
            Q(name__icontains=search_query) |
            Q(level__icontains=search_query) |
            Q(teacher__icontains=search_query)
        )
    
    # Filter by level
    level_filter = request.GET.get('level', '')
    if level_filter:
        classes = classes.filter(level=level_filter)
    
    # Filter by academic year
    year_filter = request.GET.get('year', '')
    if year_filter:
        classes = classes.filter(academic_year__id=year_filter)
    
    # Statistics
    total_classes = classes.count()
    total_students = sum([c.student_count for c in classes])


@login_required
def generate_report_card_pdf(request, pk):
    """Generate a downloadable PDF report card for a student for the latest term (or specified term via ?term=)`"""
    school = request.user.school
    student = get_object_or_404(__import__('apps.students.models', fromlist=['Student']).Student, pk=pk, school=school)

    term_id = request.GET.get('term')
    if term_id:
        term = get_object_or_404(Term, pk=term_id, school=school)
    else:
        term = Term.objects.filter(school=school).order_by('-start_date').first()

    # Grades for this student and term
    grades = Grade.objects.filter(student=student, term=term).select_related('subject') if term else []

    # Calculate weighted average
    total_weighted = 0.0
    total_coeff = 0.0
    for g in grades:
        coeff = getattr(g.subject, 'coefficient', 1)
        total_weighted += (g.score or 0) * coeff
        total_coeff += coeff
    average = round(total_weighted / total_coeff, 2) if total_coeff > 0 else 0

    # Calculate class rank (students with same grade string)
    classmates = __import__('apps.students.models', fromlist=['Student']).Student.objects.filter(school=school, grade=student.grade)
    ranking = []
    for s in classmates:
        s_grades = Grade.objects.filter(student=s, term=term).select_related('subject') if term else []
        tw = 0.0
        tc = 0.0
        for sg in s_grades:
            c = getattr(sg.subject, 'coefficient', 1)
            tw += (sg.score or 0) * c
            tc += c
        avg = round(tw / tc, 2) if tc > 0 else 0
        ranking.append({'student': s, 'average': avg})
    ranking.sort(key=lambda x: x['average'], reverse=True)
    rank = next((i + 1 for i, r in enumerate(ranking) if r['student'].pk == student.pk), None)

    # Determine mention (simple)
    def get_mention(avg):
        if avg >= 18:
            return 'Excellent'
        if avg >= 16:
            return 'Très Bien'
        if avg >= 14:
            return 'Bien'
        if avg >= 12:
            return 'Assez Bien'
        if avg >= 10:
            return 'Passable'
        return 'Faible'

    mention = get_mention(average)

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 2 * cm
    y = height - margin

    # Header
    p.setFont('Helvetica-Bold', 16)
    p.drawString(margin, y, f"Bulletin de notes - {student.full_name}")
    p.setFont('Helvetica', 10)
    y -= 1.2 * cm
    p.drawString(margin, y, f"ID Élève: {student.student_id}")
    p.drawString(width / 2, y, f"Classe: {student.grade}")
    y -= 0.8 * cm
    if term:
        p.drawString(margin, y, f"Trimestre: {term.name}")
    y -= 1 * cm

    # Table header
    p.setFont('Helvetica-Bold', 11)
    p.drawString(margin, y, 'Matière')
    p.drawString(margin + 8 * cm, y, 'Coef.')
    p.drawString(margin + 10 * cm, y, 'Note /20')
    y -= 0.6 * cm
    p.setFont('Helvetica', 10)

    for g in grades:
        if y < margin + 3 * cm:
            p.showPage()
            y = height - margin
        subj = g.subject.name if g.subject else 'N/A'
        coeff = getattr(g.subject, 'coefficient', 1)
        p.drawString(margin, y, subj)
        p.drawString(margin + 8 * cm, y, str(coeff))
        p.drawString(margin + 10 * cm, y, f"{g.score}")
        y -= 0.6 * cm

    y -= 0.6 * cm
    p.setFont('Helvetica-Bold', 11)
    p.drawString(margin, y, f"Moyenne pondérée: {average} /20")
    p.drawString(margin + 8 * cm, y, f"Rang: {rank or 'N/A'}")
    p.drawString(margin + 12 * cm, y, f"Mention: {mention}")
    y -= 1.2 * cm

    # Signature
    p.setFont('Helvetica', 10)
    p.drawString(margin, y, "Signature du directeur:")
    p.line(margin + 4 * cm, y - 2, margin + 12 * cm, y - 2)

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"bulletin_{student.student_id}_{term.name if term else 'all'}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
    
    context = {
        'classes': classes,
        'search_query': search_query,
        'level_filter': level_filter,
        'year_filter': year_filter,
        'total_classes': total_classes,
        'total_students': total_students,
        'levels': Class.LEVEL_CHOICES,
        'academic_years': school.academic_years.all(),
    }
    
    return render(request, 'academics/class_list.html', context)


@login_required
def class_detail(request, pk):
    """View class details"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=pk, school=school)
    
    # Get subjects for this class
    class_subjects = class_obj.class_subjects.select_related('subject')
    
    context = {
        'class': class_obj,
        'class_subjects': class_subjects,
        'student_count': class_obj.student_count,
        'available_spots': class_obj.available_spots,
        'is_full': class_obj.is_full,
    }
    
    return render(request, 'academics/class_detail.html', context)


@login_required
@permission_required('academics.add_class', raise_exception=True)
def class_create(request):
    """Create a new class"""
    school = request.user.school
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.school = school
            class_obj.save()
            messages.success(request, f"Classe '{class_obj.name}' créée avec succès.")
            return redirect('academics:class_detail', pk=class_obj.pk)
    else:
        form = ClassForm()
        # Filter academic years for this school
        form.fields['academic_year'].queryset = AcademicYear.objects.filter(school=school)
    
    context = {'form': form, 'action': 'Créer'}
    return render(request, 'academics/class_form.html', context)


@login_required
@permission_required('academics.change_class', raise_exception=True)
def class_update(request, pk):
    """Update a class"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=pk, school=school)
    
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Classe '{class_obj.name}' mise à jour avec succès.")
            return redirect('academics:class_detail', pk=class_obj.pk)
    else:
        form = ClassForm(instance=class_obj)
        form.fields['academic_year'].queryset = AcademicYear.objects.filter(school=school)
    
    context = {'form': form, 'class': class_obj, 'action': 'Modifier'}
    return render(request, 'academics/class_form.html', context)


@login_required
@permission_required('academics.delete_class', raise_exception=True)
def class_delete(request, pk):
    """Delete a class"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=pk, school=school)
    
    if request.method == 'POST':
        name = class_obj.name
        class_obj.delete()
        messages.success(request, f"Classe '{name}' supprimée avec succès.")
        return redirect('academics:class_list')
    
    context = {'class': class_obj}
    return render(request, 'academics/class_confirm_delete.html', context)


# ==================== SUBJECTS VIEWS ====================

@login_required
def subject_list(request):
    """List all subjects for the school"""
    school = request.user.school
    subjects = Subject.objects.filter(school=school)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query)
        )
    
    # Filter by coefficient
    coeff_filter = request.GET.get('coefficient', '')
    if coeff_filter:
        subjects = subjects.filter(coefficient=float(coeff_filter))
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        subjects = subjects.filter(is_active=True)
    elif status_filter == 'inactive':
        subjects = subjects.filter(is_active=False)
    
    # Get unique coefficients for filter
    coefficients = Subject.COEFFICIENT_CHOICES
    
    context = {
        'subjects': subjects,
        'search_query': search_query,
        'coeff_filter': coeff_filter,
        'status_filter': status_filter,
        'coefficients': coefficients,
        'total_subjects': subjects.count(),
    }
    
    return render(request, 'academics/subject_list.html', context)


@login_required
def subject_detail(request, pk):
    """View subject details"""
    school = request.user.school
    subject = get_object_or_404(Subject, pk=pk, school=school)
    
    # Get classes that have this subject
    class_subjects = subject.class_subjects.select_related('class_obj')
    
    context = {
        'subject': subject,
        'class_subjects': class_subjects,
        'class_count': class_subjects.count(),
    }
    
    return render(request, 'academics/subject_detail.html', context)


@login_required
@permission_required('academics.add_subject', raise_exception=True)
def subject_create(request):
    """Create a new subject"""
    school = request.user.school
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.school = school
            subject.save()
            messages.success(request, f"Matière '{subject.name}' créée avec succès.")
            return redirect('academics:subject_detail', pk=subject.pk)
    else:
        form = SubjectForm()
    
    context = {'form': form, 'action': 'Créer'}
    return render(request, 'academics/subject_form.html', context)


@login_required
@permission_required('academics.change_subject', raise_exception=True)
def subject_update(request, pk):
    """Update a subject"""
    school = request.user.school
    subject = get_object_or_404(Subject, pk=pk, school=school)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f"Matière '{subject.name}' mise à jour avec succès.")
            return redirect('academics:subject_detail', pk=subject.pk)
    else:
        form = SubjectForm(instance=subject)
    
    context = {'form': form, 'subject': subject, 'action': 'Modifier'}
    return render(request, 'academics/subject_form.html', context)


@login_required
@permission_required('academics.delete_subject', raise_exception=True)
def subject_delete(request, pk):
    """Delete a subject"""
    school = request.user.school
    subject = get_object_or_404(Subject, pk=pk, school=school)
    
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Matière '{name}' supprimée avec succès.")
        return redirect('academics:subject_list')
    
    context = {'subject': subject}
    return render(request, 'academics/subject_confirm_delete.html', context)


# ==================== CLASS SUBJECT VIEWS ====================

@login_required
def class_subject_create(request, class_pk):
    """Add a subject to a class"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=class_pk, school=school)
    
    if request.method == 'POST':
        form = ClassSubjectForm(request.POST)
        if form.is_valid():
            class_subject = form.save(commit=False)
            class_subject.class_obj = class_obj
            class_subject.save()
            messages.success(request, f"Matière ajoutée à la classe.")
            return redirect('academics:class_detail', pk=class_obj.pk)
    else:
        form = ClassSubjectForm()
        # Filter subjects for this school
        form.fields['subject'].queryset = Subject.objects.filter(school=school, is_active=True)
    
    context = {'form': form, 'class': class_obj, 'action': 'Ajouter'}
    return render(request, 'academics/class_subject_form.html', context)


@login_required
def class_subject_update(request, class_pk, subject_pk):
    """Update class subject"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=class_pk, school=school)
    class_subject = get_object_or_404(
        ClassSubject,
        class_obj=class_obj,
        subject__pk=subject_pk
    )
    
    if request.method == 'POST':
        form = ClassSubjectForm(request.POST, instance=class_subject)
        if form.is_valid():
            form.save()
            messages.success(request, f"Matière mise à jour.")
            return redirect('academics:class_detail', pk=class_obj.pk)
    else:
        form = ClassSubjectForm(instance=class_subject)
        form.fields['subject'].queryset = Subject.objects.filter(school=school)
    
    context = {'form': form, 'class': class_obj, 'action': 'Modifier'}
    return render(request, 'academics/class_subject_form.html', context)


@login_required
def class_subject_delete(request, class_pk, subject_pk):
    """Remove a subject from a class"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=class_pk, school=school)
    class_subject = get_object_or_404(
        ClassSubject,
        class_obj=class_obj,
        subject__pk=subject_pk
    )
    
    if request.method == 'POST':
        class_subject.delete()
        messages.success(request, f"Matière supprimée de la classe.")
        return redirect('academics:class_detail', pk=class_obj.pk)
    
    context = {'class_subject': class_subject, 'class': class_obj}
    return render(request, 'academics/class_subject_confirm_delete.html', context)


# ==================== GRADES VIEWS ====================

@login_required
def grade_list(request):
    """List all grades for students"""
    school = request.user.school
    grades = Grade.objects.filter(school=school).select_related('student', 'subject', 'term')
    
    # Filter by term
    term_filter = request.GET.get('term', '')
    if term_filter:
        grades = grades.filter(term__id=term_filter)
    
    # Filter by student
    student_filter = request.GET.get('student', '')
    if student_filter:
        grades = grades.filter(student__id=student_filter)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        grades = grades.filter(
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query)
        )
    
    terms = Term.objects.filter(school=school)
    
    context = {
        'grades': grades,
        'terms': terms,
        'term_filter': term_filter,
        'student_filter': student_filter,
        'search_query': search_query,
    }
    
    return render(request, 'academics/grade_list.html', context)


@login_required
@permission_required('academics.add_grade', raise_exception=True)
def grade_create(request):
    """Create a new grade"""
    school = request.user.school
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.school = school
            grade.save()
            messages.success(request, f"Note créée avec succès.")
            return redirect('academics:student_results', pk=grade.student.pk)
    else:
        form = GradeForm()
        # Filter by school
        from apps.students.models import Student
        form.fields['student'].queryset = Student.objects.filter(school=school)
        form.fields['subject'].queryset = Subject.objects.filter(school=school)
        form.fields['term'].queryset = Term.objects.filter(school=school)
    
    context = {'form': form, 'action': 'Créer'}
    return render(request, 'academics/grade_form.html', context)


@login_required
@permission_required('academics.change_grade', raise_exception=True)
def grade_update(request, pk):
    """Update a grade"""
    school = request.user.school
    grade = get_object_or_404(Grade, pk=pk, school=school)
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note mise à jour avec succès.")
            return redirect('academics:student_results', pk=grade.student.pk)
    else:
        form = GradeForm(instance=grade)
        from apps.students.models import Student
        form.fields['student'].queryset = Student.objects.filter(school=school)
        form.fields['subject'].queryset = Subject.objects.filter(school=school)
        form.fields['term'].queryset = Term.objects.filter(school=school)
    
    context = {'form': form, 'grade': grade, 'action': 'Modifier'}
    return render(request, 'academics/grade_form.html', context)


@login_required
@permission_required('academics.delete_grade', raise_exception=True)
def grade_delete(request, pk):
    """Delete a grade"""
    school = request.user.school
    grade = get_object_or_404(Grade, pk=pk, school=school)
    student = grade.student
    
    if request.method == 'POST':
        grade.delete()
        messages.success(request, f"Note supprimée avec succès.")
        return redirect('academics:student_results', pk=student.pk)
    
    context = {'grade': grade}
    return render(request, 'academics/grade_confirm_delete.html', context)


@login_required
def student_results(request, pk):
    """View student results and average"""
    from apps.students.models import Student
    school = request.user.school
    student = get_object_or_404(Student, pk=pk, school=school)
    
    # Get all grades for this student
    grades = Grade.objects.filter(student=student).select_related('subject', 'term')
    
    # Group by term
    terms = Term.objects.filter(school=school).order_by('academic_year', 'term_number')
    
    # Calculate weighted average per term
    term_results = {}
    for term in terms:
        term_grades = grades.filter(term=term)
        if term_grades.exists():
            # Calculate weighted average
            total_weighted_score = 0
            total_coefficient = 0
            
            for grade in term_grades:
                total_weighted_score += grade.score * grade.subject.coefficient
                total_coefficient += grade.subject.coefficient
            
            average = round(total_weighted_score / total_coefficient, 2) if total_coefficient > 0 else 0
            
            term_results[term] = {
                'grades': term_grades,
                'average': average,
                'rating': get_rating(average),
            }
    
    # Get class and ranking
    class_obj = student.class_name if hasattr(student, 'class_name') else None
    
    context = {
        'student': student,
        'term_results': term_results,
        'class': class_obj,
        'all_grades': grades,
    }
    
    return render(request, 'academics/student_results.html', context)


@login_required
def class_results(request, class_pk):
    """View all results for a class"""
    school = request.user.school
    class_obj = get_object_or_404(Class, pk=class_pk, school=school)
    
    # Get term filter
    term_filter = request.GET.get('term', '')
    
    # Get all students in class
    from apps.students.models import Student
    students = Student.objects.filter(school=school)
    
    # Get students by class (if class relationship exists)
    # This depends on how students are linked to classes in the students app
    
    terms = Term.objects.filter(school=school).order_by('academic_year', 'term_number')
    
    # Calculate results for each student
    class_results_data = []
    
    if term_filter:
        term = get_object_or_404(Term, pk=term_filter, school=school)
        
        for student in students:
            grades = Grade.objects.filter(student=student, term=term)
            
            if grades.exists():
                total_weighted_score = 0
                total_coefficient = 0
                
                for grade in grades:
                    total_weighted_score += grade.score * grade.subject.coefficient
                    total_coefficient += grade.subject.coefficient
                
                average = round(total_weighted_score / total_coefficient, 2) if total_coefficient > 0 else 0
                
                class_results_data.append({
                    'student': student,
                    'average': average,
                    'rating': get_rating(average),
                })
        
        # Sort by average (descending) and add ranking
        class_results_data.sort(key=lambda x: x['average'], reverse=True)
        for rank, result in enumerate(class_results_data, 1):
            result['rank'] = rank
    
    context = {
        'class': class_obj,
        'results': class_results_data,
        'terms': terms,
        'term_filter': term_filter,
    }
    
    return render(request, 'academics/class_results.html', context)


def get_rating(average):
    """Get rating label for an average score"""
    if average >= 18:
        return 'Excellent'
    elif average >= 16:
        return 'Très Bien'
    elif average >= 14:
        return 'Bien'
    elif average >= 12:
        return 'Assez Bien'
    elif average >= 10:
        return 'Passable'
    else:
        return 'Faible'
