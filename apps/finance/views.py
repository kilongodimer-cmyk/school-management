from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from django.db.models import Sum
from django.urls import reverse
from .models import Payment
from .forms import PaymentForm
from apps.students.models import Student


@login_required
@role_required(['accountant', 'director', 'superadmin'])
def payment_create(request):
    school = request.user.school
    if request.method == 'POST':
        form = PaymentForm(request.POST, school=school)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.school = school
            payment.save()
            return redirect(reverse('finance:payments_list'))
    else:
        form = PaymentForm(school=school)

    return render(request, 'finance/payment_form.html', {'form': form})


@login_required
@role_required(['accountant', 'director', 'superadmin'])
def payments_list(request):
    school = request.user.school
    payments = Payment.objects.filter(school=school).select_related('student')
    return render(request, 'finance/payments_list.html', {'payments': payments})


@login_required
@role_required(['accountant', 'director', 'superadmin', 'teacher'])
def student_payments(request, student_id):
    school = request.user.school
    student = get_object_or_404(Student, pk=student_id, school=school)
    payments = student.payments.filter(school=school).order_by('-payment_date')
    total = payments.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'finance/student_payments.html', {'student': student, 'payments': payments, 'total': total})


@login_required
@role_required(['accountant', 'director', 'superadmin'])
def debtor_list(request):
    school = request.user.school
    # Simple debtor definition: students with no payments
    debtors = Student.objects.filter(school=school).annotate(total_paid=Sum('payments__amount')).filter(total_paid__isnull=True)
    return render(request, 'finance/debtor_list.html', {'debtors': debtors})


@login_required
@role_required(['accountant', 'director', 'superadmin'])
def dashboard(request):
    school = request.user.school
    # Total collected
    total_collected = Payment.objects.filter(school=school).aggregate(total=Sum('amount'))['total'] or 0

    # Counts
    from apps.students.models import Student
    from apps.accounts.models import CustomUser

    total_students = Student.objects.filter(school=school).count()
    total_teachers = CustomUser.objects.filter(school=school, role='teacher').count()

    # Students in arrears: no payments or zero total
    debtors_qs = Student.objects.filter(school=school).annotate(total_paid=Sum('payments__amount')).filter(total_paid__isnull=True)
    debtors_count = debtors_qs.count()

    # School average (use student.gpa when available)
    avg_gpa = Student.objects.filter(school=school).aggregate(avg=Avg('gpa'))['avg']
    avg_gpa = round(avg_gpa, 2) if avg_gpa is not None else 0

    recent_payments = Payment.objects.filter(school=school).select_related('student')[:10]

    context = {
        'total_collected': total_collected,
        'recent_payments': recent_payments,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'debtors_count': debtors_count,
        'avg_gpa': avg_gpa,
    }

    return render(request, 'finance/dashboard.html', context)
