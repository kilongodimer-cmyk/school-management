from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import School
from apps.accounts.models import CustomUser


class Student(models.Model):
    """
    Modèle représentant un élève dans l'école
    Lié à une école spécifique et un utilisateur parent/tuteur optionnel
    """
    
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
        ('graduated', 'Diplômé'),
        ('suspended', 'Suspendu'),
    ]
    
    # Information de base
    first_name = models.CharField(
        max_length=100,
        verbose_name='Prénom'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Nom'
    )
    student_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Numéro d\'élève'
    )
    
    # École et classe
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='students',
        verbose_name='École'
    )
    grade = models.CharField(
        max_length=50,
        verbose_name='Classe/Niveau',
        help_text='Ex: 6ème A, Terminale S, etc.'
    )
    
    # Information personnelle
    date_of_birth = models.DateField(
        verbose_name='Date de naissance'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
        verbose_name='Genre'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone'
    )
    
    # Adresse
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Adresse'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ville'
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Code postal'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Pays'
    )
    
    # Contact parent/tuteur
    parent_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nom du parent/tuteur'
    )
    parent_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone du parent'
    )
    parent_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email du parent'
    )
    
    # Informations académiques
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name='Date d\'inscription'
    )
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Moyenne générale'
    )
    
    # Photo
    photo = models.ImageField(
        upload_to='students/photos/',
        blank=True,
        null=True,
        verbose_name='Photo'
    )
    
    # Status et notes
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Statut'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    
    # Horodatage
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Créé le'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modifié le'
    )
    
    class Meta:
        verbose_name = 'Élève'
        verbose_name_plural = 'Élèves'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['school', 'grade']),
            models.Index(fields=['school', 'status']),
            models.Index(fields=['student_id']),
        ]
        permissions = [
            ('view_student_reports', 'Peut voir les rapports des élèves'),
            ('export_students', 'Peut exporter les élèves'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate student age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def full_address(self):
        """Return complete address"""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        return ', '.join(parts) if parts else 'N/A'
    
    def get_gender_display_icon(self):
        """Return gender icon"""
        icons = {
            'M': '<i class="fas fa-mars"></i>',
            'F': '<i class="fas fa-venus"></i>',
            'O': '<i class="fas fa-genderless"></i>',
        }
        return icons.get(self.gender, '-')
    
    def is_active_student(self):
        return self.status == 'active'
    
    def can_enroll(self):
        return self.status in ['active', 'graduated']
