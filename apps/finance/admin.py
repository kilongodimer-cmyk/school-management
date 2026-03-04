from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_type', 'payment_date', 'school')
    list_filter = ('payment_type', 'payment_date', 'school')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')
    readonly_fields = ('created_at', 'updated_at')
