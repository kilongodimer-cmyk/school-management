from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.accounts.models import School
from datetime import datetime


class AcademicYear(models.Model):
    """Année académique"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    year = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(datetime.now().year + 10)
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('school', 'year')]
        ordering = ['-year']
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

    def __str__(self):
        return f"{self.year} ({self.school.name})"

    @property
    def is_current(self):
        """Check if academic year is current"""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Class(models.Model):
    """Model pour les classes"""
    LEVEL_CHOICES = [
        ('1', 'Niveau 1 (Reception)'),
        ('2', 'Niveau 2'),
        ('3', 'Niveau 3'),
        ('4', 'Niveau 4'),
        ('5', 'Niveau 5'),
        ('6', 'Niveau 6'),
        ('7', 'Niveau 7'),
        ('8', 'Niveau 8'),
        ('9', 'Niveau 9'),
        ('10', 'Niveau 10 (SEC 1)'),
        ('11', 'Niveau 11 (SEC 2)'),
        ('12', 'Niveau 12 (SEC 3)'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=50, help_text="Ex: 6ème A, Première S")
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        help_text="Niveau académique"
    )
    room = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Numéro ou nom de la salle"
    )
    capacity = models.PositiveIntegerField(
        default=40,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        help_text="Capacité maximale"
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        related_name='classes'
    )
    teacher = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Professeur principal"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('school', 'name')]
        ordering = ['level', 'name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        indexes = [
            models.Index(fields=['school', 'level']),
            models.Index(fields=['school', 'academic_year']),
        ]

    def __str__(self):
        return f"{self.name} ({self.school.name})"

    @property
    def full_name(self):
        return f"{self.name} - Niveau {self.level}"

    @property
    def student_count(self):
        """Count students in this class"""
        return self.students.count()

    @property
    def available_spots(self):
        """Available spots in class"""
        return max(0, self.capacity - self.student_count)

    @property
    def is_full(self):
        """Check if class is full"""
        return self.student_count >= self.capacity


class Subject(models.Model):
    """Model pour les matières"""
    COEFFICIENT_CHOICES = [
        (0.5, '0.5'),
        (1, '1'),
        (1.5, '1.5'),
        (2, '2'),
        (2.5, '2.5'),
        (3, '3'),
        (3.5, '3.5'),
        (4, '4'),
        (5, '5'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100, help_text="Ex: Mathématiques, Français")
    code = models.CharField(
        max_length=20,
        help_text="Code unique (ex: MATH, FR)"
    )
    coefficient = models.FloatField(
        choices=COEFFICIENT_CHOICES,
        default=1,
        help_text="Coefficient pour le calcul de moyenne"
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('school', 'code')]
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        indexes = [
            models.Index(fields=['school', 'code']),
            models.Index(fields=['school', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.code}) - Coeff: {self.coefficient}"


class ClassSubject(models.Model):
    """Relation entre classes et matières"""
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    teacher = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Professeur de cette matière dans cette classe"
    )
    hours_per_week = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Heures par semaine"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('class_obj', 'subject')]
        verbose_name = 'Class Subject'
        verbose_name_plural = 'Class Subjects'
        ordering = ['class_obj', 'subject']

    def __str__(self):
        return f"{self.class_obj.name} - {self.subject.name}"


class Term(models.Model):
    """Model pour les termes/trimestres"""
    TERM_CHOICES = [
        ('1', 'Trimestre 1'),
        ('2', 'Trimestre 2'),
        ('3', 'Trimestre 3'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='terms')
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='terms'
    )
    term_number = models.CharField(max_length=1, choices=TERM_CHOICES)
    name = models.CharField(max_length=50, help_text="Ex: Trimestre 1")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('academic_year', 'term_number')]
        ordering = ['academic_year', 'term_number']
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return f"{self.name} ({self.academic_year.year})"

    @property
    def is_current(self):
        """Check if term is current"""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Grade(models.Model):
    """Model pour les notes des élèves"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='grades'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Score sur 20"
    )
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('student', 'subject', 'term')]
        ordering = ['student', 'subject', 'term']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        indexes = [
            models.Index(fields=['student', 'term']),
            models.Index(fields=['school', 'term']),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.code} ({self.term.name}): {self.score}"

    @property
    def rating(self):
        """Get rating for score (Excellent, Bien, etc)"""
        if self.score >= 18:
            return 'Excellent'
        elif self.score >= 16:
            return 'Très Bien'
        elif self.score >= 14:
            return 'Bien'
        elif self.score >= 12:
            return 'Assez Bien'
        elif self.score >= 10:
            return 'Passable'
        else:
            return 'Faible'

    @property
    def status_badge(self):
        """Get CSS color for score"""
        if self.score >= 16:
            return 'success'
        elif self.score >= 12:
            return 'info'
        elif self.score >= 10:
            return 'warning'
        else:
            return 'danger'
