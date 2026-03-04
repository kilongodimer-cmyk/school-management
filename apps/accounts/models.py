"""
Modèles pour l'application accounts
- School : Représente une école
- CustomUser : Utilisateur personnalisé avec rôles
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class School(models.Model):
    """
    Modèle pour représenter une école dans le système SaaS
    """
    
    class Meta:
        verbose_name = _("École")
        verbose_name_plural = _("Écoles")
        ordering = ['name']

    name = models.CharField(
        _("Nom de l'école"),
        max_length=255,
        unique=True,
        help_text=_("Nom complet de l'établissement")
    )
    
    code = models.CharField(
        _("Code de l'école"),
        max_length=50,
        unique=True,
        help_text=_("Code unique pour identifier l'école")
    )
    
    email = models.EmailField(
        _("Email de l'école"),
        unique=True,
        help_text=_("Email principal de contact")
    )
    
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Numéro de téléphone de l'école")
    )
    
    address = models.TextField(
        _("Adresse"),
        blank=True,
        null=True,
        help_text=_("Adresse complète de l'école")
    )
    
    city = models.CharField(
        _("Ville"),
        max_length=100,
        blank=True,
        null=True
    )
    
    country = models.CharField(
        _("Pays"),
        max_length=100,
        blank=True,
        null=True
    )
    
    postal_code = models.CharField(
        _("Code postal"),
        max_length=20,
        blank=True,
        null=True
    )
    
    director_name = models.CharField(
        _("Nom du directeur"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Nom du directeur ou responsable principal")
    )
    
    logo = models.ImageField(
        _("Logo"),
        upload_to='schools/logos/%Y/%m/',
        blank=True,
        null=True,
        help_text=_("Logo de l'établissement")
    )
    
    website = models.URLField(
        _("Site web"),
        blank=True,
        null=True,
        help_text=_("Adresse du site web de l'école")
    )
    
    max_students = models.IntegerField(
        _("Nombre maximum d'étudiants"),
        default=1000,
        help_text=_("Limite de la capacité de l'école")
    )
    
    max_teachers = models.IntegerField(
        _("Nombre maximum d'enseignants"),
        default=100,
        help_text=_("Limite du nombre d'enseignants")
    )
    
    is_active = models.BooleanField(
        _("Actif"),
        default=True,
        help_text=_("Indique si l'école est active")
    )
    
    created_at = models.DateTimeField(
        _("Créé le"),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _("Modifié le"),
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec rôles et association à une école
    Hérite de AbstractUser pour bénéficier des fonctionnalités Django
    """
    
    ROLE_CHOICES = [
        ('superadmin', _('Super Admin')),
        ('director', _('Directeur')),
        ('teacher', _('Enseignant')),
        ('accountant', _('Comptable')),
        ('student', _('Étudiant')),
        ('parent', _('Parent')),
    ]

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['school', 'role']),
            models.Index(fields=['email']),
        ]

    # Override M2M fields to fix related_name clash with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_("The groups this user belongs to. A user will get all permissions granted to each of their groups."),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="customuser_set",
        related_query_name="customuser",
    )

    # Lien vers l'école (nullable pour les superadmins)
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True,
        verbose_name=_("École"),
        help_text=_("L'école à laquelle l'utilisateur appartient")
    )

    # Rôle de l'utilisateur
    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text=_("Le rôle de l'utilisateur dans le système")
    )

    # Informations additionnelles
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Numéro de téléphone personnel")
    )

    address = models.TextField(
        _("Adresse"),
        blank=True,
        null=True,
        help_text=_("Adresse personnelle")
    )

    city = models.CharField(
        _("Ville"),
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        _("Pays"),
        max_length=100,
        blank=True,
        null=True
    )

    postal_code = models.CharField(
        _("Code postal"),
        max_length=20,
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(
        _("Photo de profil"),
        upload_to='users/profiles/%Y/%m/',
        blank=True,
        null=True,
        help_text=_("Photo de profil de l'utilisateur")
    )

    bio = models.TextField(
        _("Biographie"),
        blank=True,
        null=True,
        max_length=500,
        help_text=_("Courte biographie ou description")
    )

    # Statuts
    is_verified = models.BooleanField(
        _("Email vérifié"),
        default=False,
        help_text=_("Indique si l'email a été vérifié")
    )

    is_banned = models.BooleanField(
        _("Compte suspendu"),
        default=False,
        help_text=_("Indique si le compte est suspendu")
    )

    # Dates
    created_at = models.DateTimeField(
        _("Créé le"),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("Modifié le"),
        auto_now=True
    )

    last_login_at = models.DateTimeField(
        _("Dernière connexion"),
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_role_display_fr(self):
        """Retourne le rôle formaté en français"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def is_superadmin(self):
        """Vérifie si l'utilisateur est super admin"""
        return self.role == 'superadmin' or self.is_superuser

    def is_director(self):
        """Vérifie si l'utilisateur est directeur"""
        return self.role == 'director'

    def is_teacher(self):
        """Vérifie si l'utilisateur est enseignant"""
        return self.role == 'teacher'

    def is_accountant(self):
        """Vérifie si l'utilisateur est comptable"""
        return self.role == 'accountant'

    def is_student(self):
        """Vérifie si l'utilisateur est étudiant"""
        return self.role == 'student'

    def is_parent(self):
        """Vérifie si l'utilisateur est parent"""
        return self.role == 'parent'

    @property
    def full_address(self):
        """Retourne l'adresse complète formatée"""
        parts = [self.address, self.postal_code, self.city, self.country]
        return ', '.join([p for p in parts if p])
