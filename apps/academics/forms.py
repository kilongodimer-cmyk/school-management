from django import forms
from .models import Class, Subject, AcademicYear, ClassSubject, Term, Grade


class AcademicYearForm(forms.ModelForm):
    """Form pour les années académiques"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de début"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de fin"
    )

    class Meta:
        model = AcademicYear
        fields = ['year', 'start_date', 'end_date', 'is_active']
        widgets = {
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'year': 'Année',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_active': 'Année active',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError("La date de fin doit être après la date de début.")

        return cleaned_data


class ClassForm(forms.ModelForm):
    """Form pour les classes"""
    
    class Meta:
        model = Class
        fields = ['name', 'level', 'room', 'capacity', 'academic_year', 'teacher', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 6ème A'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Salle 101'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '40'
            }),
            'academic_year': forms.Select(attrs={
                'class': 'form-select'
            }),
            'teacher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du professeur principal'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la classe'
            }),
        }
        labels = {
            'name': 'Nom de la classe',
            'level': 'Niveau',
            'room': 'Salle',
            'capacity': 'Capacité',
            'academic_year': 'Année académique',
            'teacher': 'Professeur principal',
            'description': 'Description',
        }

    def clean_name(self):
        """Validate class name"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise forms.ValidationError("Le nom de la classe doit avoir au moins 2 caractères.")
        return name

    def clean_capacity(self):
        """Validate capacity"""
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity < 1:
            raise forms.ValidationError("La capacité doit être au moins 1.")
        return capacity


class SubjectForm(forms.ModelForm):
    """Form pour les matières"""
    
    class Meta:
        model = Subject
        fields = ['name', 'code', 'coefficient', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Mathématiques'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: MATH'
            }),
            'coefficient': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la matière'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'name': 'Nom de la matière',
            'code': 'Code',
            'coefficient': 'Coefficient',
            'description': 'Description',
            'is_active': 'Matière active',
        }

    def clean_code(self):
        """Validate code"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            if len(code) < 2:
                raise forms.ValidationError("Le code doit avoir au moins 2 caractères.")
        return code

    def clean_name(self):
        """Validate name"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise forms.ValidationError("Le nom doit avoir au moins 2 caractères.")
        return name


class ClassSubjectForm(forms.ModelForm):
    """Form pour lier les matières aux classes"""
    
    class Meta:
        model = ClassSubject
        fields = ['subject', 'teacher', 'hours_per_week', 'is_active']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'teacher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du professeur'
            }),
            'hours_per_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'subject': 'Matière',
            'teacher': 'Professeur',
            'hours_per_week': 'Heures par semaine',
            'is_active': 'Actif',
        }

    def clean_hours_per_week(self):
        """Validate hours"""
        hours = self.cleaned_data.get('hours_per_week')
        if hours and hours < 1:
            raise forms.ValidationError("Les heures doivent être au moins 1.")
        return hours


class TermForm(forms.ModelForm):
    """Form pour les termes/trimestres"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de début"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Date de fin"
    )

    class Meta:
        model = Term
        fields = ['term_number', 'name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'term_number': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Trimestre 1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'term_number': 'Numéro du trimestre',
            'name': 'Nom',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_active': 'Trimestre actif',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError("La date de fin doit être après la date de début.")

        return cleaned_data


class GradeForm(forms.ModelForm):
    """Form pour les notes"""
    
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'term', 'score', 'comments']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'term': forms.Select(attrs={
                'class': 'form-select'
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '15',
                'min': '0',
                'max': '20',
                'step': '0.5'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaires optionnels'
            }),
        }
        labels = {
            'student': 'Élève',
            'subject': 'Matière',
            'term': 'Trimestre',
            'score': 'Note (0-20)',
            'comments': 'Commentaires',
        }

    def clean_score(self):
        """Validate score"""
        score = self.cleaned_data.get('score')
        if score is not None:
            if score < 0 or score > 20:
                raise forms.ValidationError("La note doit être entre 0 et 20.")
        return score

