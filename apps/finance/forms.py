from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.school = school
        if school is not None:
            # restrict student choices to the school when provided
            self.fields['student'].queryset = Student.objects.filter(school=school)

    class Meta:
        model = Payment
        fields = ['student', 'amount', 'payment_type', 'payment_date', 'notes']
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean_amount(self):
        amt = self.cleaned_data.get('amount')
        if amt is None or amt <= 0:
            raise forms.ValidationError('Le montant doit être supérieur à 0.')
        return amt

    def clean_student(self):
        student = self.cleaned_data.get('student')
        if self.school and student and student.school_id != self.school.id:
            raise forms.ValidationError('L\'élève sélectionné n\'appartient pas à votre établissement.')
        return student
