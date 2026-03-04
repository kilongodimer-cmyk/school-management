from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('tuition', 'Tuition'),
        ('enrollment', 'Enrollment'),
        ('other', 'Other'),
    ]

    school = models.ForeignKey('accounts.School', on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='tuition')
    payment_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
        indexes = [models.Index(fields=['student', 'payment_date']), models.Index(fields=['school', 'payment_date'])]

    def __str__(self):
        return f"{self.student} — {self.amount} ({self.get_payment_type_display()})"
