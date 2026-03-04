from django import forms
from django.core.exceptions import ValidationError
from .models import Student
from datetime import date


class StudentForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier un étudiant
    """
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'student_id',
            'grade', 'date_of_birth', 'gender', 'email', 'phone',
            'address', 'city', 'postal_code', 'country',
            'parent_name', 'parent_phone', 'parent_email',
            'gpa', 'photo', 'status', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom',
                'required': True
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: STU-2024-001',
                'required': True
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 6ème A, Terminale S',
                'required': True
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code postal'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pays'
            }),
            'parent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du parent/tuteur'
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone du parent'
            }),
            'parent_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email du parent'
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Moyenne générale (0-20)',
                'step': '0.01',
                'min': '0',
                'max': '20'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Notes supplémentaires',
                'rows': 4
            }),
        }
    
    def clean_date_of_birth(self):
        """Valider que la date de naissance n'est pas dans le futur"""
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise ValidationError('La date de naissance ne peut pas être dans le futur.')
        return date_of_birth
    
    def clean_student_id(self):
        """Valider l'unicité du numéro d'élève"""
        student_id = self.cleaned_data.get('student_id')
        # Vérifier l'unicité globale
        qs = Student.objects.filter(student_id=student_id)
        # Exclure l'instance courante si elle existe
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ce numéro d\'élève existe déjà.')
        return student_id
    
    def clean(self):
        cleaned_data = super().clean()
        gpa = cleaned_data.get('gpa')
        if gpa and (gpa < 0 or gpa > 20):
            raise ValidationError('La moyenne générale doit être entre 0 et 20.')
        return cleaned_data


class StudentSearchForm(forms.Form):
    """
    Formulaire pour rechercher et filtrer les élèves
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par nom ou numéro d\'élève...'
        }),
        label='Recherche'
    )
    
    grade = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filtrer par classe...'
        }),
        label='Classe'
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les statuts')] + list(Student.STATUS_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Statut'
    )
    
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les genres')] + list(Student.GENDER_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Genre'
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('last_name', 'Nom (A-Z)'),
            ('-last_name', 'Nom (Z-A)'),
            ('first_name', 'Prénom (A-Z)'),
            ('-gpa', 'Moyenne générale (Plus haut)'),
            ('gpa', 'Moyenne générale (Plus bas)'),
            ('-created_at', 'Plus récemment inscrit'),
            ('created_at', 'Plus anciennement inscrit'),
        ],
        initial='last_name',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Trier par'
    )


class BulkStudentActionForm(forms.Form):
    """
    Formulaire pour les actions en masse sur les élèves
    """
    ACTION_CHOICES = [
        ('', '-- Sélectionner une action --'),
        ('activate', 'Activer'),
        ('deactivate', 'Désactiver'),
        ('graduate', 'Diplômer'),
        ('suspend', 'Suspendre'),
        ('export', 'Exporter'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )


class StudentFilterForm(forms.Form):
    """
    Formulaire avancé pour filtrer les élèves
    """
    FILTER_CHOICES = [
        ('', 'Tous les élèves'),
        ('active', 'Actifs'),
        ('inactive', 'Inactifs'),
        ('graduated', 'Diplômés'),
        ('suspended', 'Suspendus'),
        ('high_gpa', 'Excellents résultats (GPA > 16)'),
        ('low_gpa', 'À suivre (GPA < 10)'),
    ]
    
    filter_type = forms.ChoiceField(
        required=False,
        choices=FILTER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Filtrer'
    )
