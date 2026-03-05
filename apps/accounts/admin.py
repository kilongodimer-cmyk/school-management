"""
Configuration admin personnalisée pour l'app accounts
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import School, CustomUser


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """Admin personnalisé pour le modèle School"""
    
    list_display = [
        'code',
        'name',
        'city',
        'director_name',
        'user_count',
        'is_active_badge',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'created_at',
        'country',
        'city'
    ]
    
    search_fields = [
        'name',
        'code',
        'email',
        'director_name',
        'city'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'user_count'
    ]
    
    fieldsets = (
        (_("Informations principales"), {
            'fields': ('name', 'code', 'email', 'phone', 'website')
        }),
        (_("Localisation"), {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        (_("Administration"), {
            'fields': ('director_name', 'logo')
        }),
        (_("Capacité"), {
            'fields': ('max_students', 'max_teachers')
        }),
        (_("Statut"), {
            'fields': ('is_active',)
        }),
        (_("Dates"), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        (_("Statistiques"), {
            'fields': ('user_count',),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    def user_count(self, obj):
        """Affiche le nombre d'utilisateurs de l'école"""
        count = obj.users.count()
        return format_html(
            '<strong>{}</strong>',
            count
        )
    user_count.short_description = _("Nombre d'utilisateurs")
    
    def is_active_badge(self, obj):
        """Affiche un badge pour le statut actif"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Actif</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Inactif</span>'
        )
    is_active_badge.short_description = _("Statut")


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin personnalisé pour le modèle CustomUser"""
    
    list_display = [
        'get_full_name_display',
        'email',
        'school_link',
        'get_role_badge',
        'is_verified_badge',
        'is_active_badge',
        'last_login'
    ]
    
    list_filter = [
        'role',
        'school',
        'is_active',
        'is_verified',
        'is_banned',
        'created_at',
    ]
    
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'school__name'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'last_login_at',
        'get_role_display_fr'
    ]
    
    fieldsets = (
        (_("Informations de connexion"), {
            'fields': ('username', 'email', 'password')
        }),
        (_("Informations personnelles"), {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'profile_photo',
                'bio'
            )
        }),
        (_("École et Rôle"), {
            'fields': ('school', 'role', 'get_role_display_fr')
        }),
        (_("Adresse"), {
            'fields': (
                'address',
                'postal_code',
                'city',
                'country'
            ),
            'classes': ('collapse',)
        }),
        (_("Permissions"), {
            'fields': (
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_("Statut"), {
            'fields': (
                'is_active',
                'is_verified',
                'is_banned'
            )
        }),
        (_("Dates"), {
            'fields': (
                'created_at',
                'updated_at',
                'last_login_at',
                'last_login'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'school',
                'role'
            ),
        }),
    )
    
    ordering = ['-created_at']
    filter_horizontal = ['groups', 'user_permissions']
    
    def get_full_name_display(self, obj):
        """Affiche le nom complet ou le username"""
        full_name = obj.get_full_name()
        return full_name if full_name.strip() else obj.username
    get_full_name_display.short_description = _("Utilisateur")
    
    def school_link(self, obj):
        """Affiche un lien vers l'école"""
        if obj.school:
            url = f'/admin/accounts/school/{obj.school.id}/change/'
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.school.name
            )
        return format_html('<em style="color: gray;">-</em>')
    school_link.short_description = _("École")
    
    def get_role_badge(self, obj):
        """Affiche un badge coloré pour le rôle"""
        colors = {
            'superadmin': '#d32f2f',  # Rouge
            'director': '#1976d2',    # Bleu
            'teacher': '#388e3c',     # Vert
            'accountant': '#f57c00',  # Orange
            'student': '#7b1fa2',     # Violet
            'parent': '#c2185b',      # Rose
        }
        color = colors.get(obj.role, '#666')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 4px; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    get_role_badge.short_description = _("Rôle")
    
    def is_verified_badge(self, obj):
        """Affiche un badge pour la vérification"""
        if obj.is_verified:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Vérifié</span>'
            )
        return format_html(
            '<span style="color: orange;">⧖ Non vérifié</span>'
        )
    is_verified_badge.short_description = _("Vérification")
    
    def is_active_badge(self, obj):
        """Affiche un badge pour le statut"""
        if obj.is_banned:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Suspendu</span>'
            )
        if obj.is_active:
            return format_html(
                '<span style="color: green;">✓ Actif</span>'
            )
        return format_html(
            '<span style="color: gray;">✗ Inactif</span>'
        )
    is_active_badge.short_description = _("Statut")
    
    def get_readonly_fields(self, request, obj=None):
        """Rendre readonly certains champs"""
        readonly = super().get_readonly_fields(request, obj=obj)
        # Les superusers peuvent modifier tous les champs
        if request.user.is_superuser:
            return readonly
        # Les autres admins ne peuvent pas modifier les dates
        return list(readonly) + ['created_at', 'updated_at']
