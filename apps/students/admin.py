from django.contrib import admin
from django.utils.html import format_html
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface personnalisé pour le modèle Student
    """
    
    list_display = [
        'student_id_display',
        'full_name_display',
        'grade_display',
        'school_display',
        'status_badge',
        'gpa_display',
        'age_display',
        'created_at_display',
    ]
    
    list_filter = [
        'school',
        'grade',
        'status',
        'gender',
        'created_at',
        'gpa',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'student_id',
        'email',
        'parent_email',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'age_display',
        'full_name_display',
    ]
    
    fieldsets = (
        ('Informations de base', {
            'fields': (
                'first_name',
                'last_name',
                'student_id',
                'full_name_display',
            )
        }),
        ('École et Classe', {
            'fields': (
                'school',
                'grade',
            )
        }),
        ('Informations personnelles', {
            'fields': (
                'date_of_birth',
                'age_display',
                'gender',
                'email',
                'phone',
                'photo',
            )
        }),
        ('Adresse', {
            'fields': (
                'address',
                'city',
                'postal_code',
                'country',
            ),
            'classes': ('collapse',)
        }),
        ('Contact parent/tuteur', {
            'fields': (
                'parent_name',
                'parent_phone',
                'parent_email',
            )
        }),
        ('Informations académiques', {
            'fields': (
                'gpa',
                'status',
            )
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Horodatage', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'make_active',
        'make_inactive',
        'mark_graduated',
        'mark_suspended',
    ]
    
    def student_id_display(self, obj):
        """Afficher l'ID de l'élève"""
        return format_html(
            '<code style="background-color: #f0f0f0; padding: 3px 6px; border-radius: 3px;">{}</code>',
            obj.student_id
        )
    student_id_display.short_description = 'Numéro d\'élève'
    
    def full_name_display(self, obj):
        """Afficher le nom complet"""
        return obj.full_name
    full_name_display.short_description = 'Nom complet'
    
    def grade_display(self, obj):
        """Afficher la classe"""
        return format_html(
            '<span style="background-color: #e7f3ff; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.grade
        )
    grade_display.short_description = 'Classe'
    
    def school_display(self, obj):
        """Afficher l'école avec lien"""
        return format_html(
            '<strong>{}</strong>',
            obj.school.name
        )
    school_display.short_description = 'École'
    
    def status_badge(self, obj):
        """Afficher le statut avec badge de couleur"""
        colors = {
            'active': '#28a745',
            'inactive': '#6c757d',
            'graduated': '#007bff',
            'suspended': '#dc3545',
        }
        status_display = dict(obj.STATUS_CHOICES).get(obj.status, obj.status)
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status_display
        )
    status_badge.short_description = 'Statut'
    
    def gpa_display(self, obj):
        """Afficher la moyenne générale avec couleur"""
        if obj.gpa is None:
            return '-'
        
        if obj.gpa >= 16:
            color = '#28a745'  # Vert
        elif obj.gpa >= 12:
            color = '#007bff'  # Bleu
        elif obj.gpa >= 10:
            color = '#ffc107'  # Jaune
        else:
            color = '#dc3545'  # Rouge
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{:.2f}</span>',
            color,
            obj.gpa
        )
    gpa_display.short_description = 'Moyenne'
    
    def age_display(self, obj):
        """Afficher l'âge"""
        return f'{obj.age} ans' if obj.age else '-'
    age_display.short_description = 'Âge'
    
    def created_at_display(self, obj):
        """Afficher la date de création"""
        return obj.created_at.strftime('%d/%m/%Y')
    created_at_display.short_description = 'Inscription'
    
    @admin.action(description='Activer les élèves sélectionnés')
    def make_active(self, request, queryset):
        """Action pour activer les élèves"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} élève(s) activé(s) avec succès.')
    
    @admin.action(description='Désactiver les élèves sélectionnés')
    def make_inactive(self, request, queryset):
        """Action pour désactiver les élèves"""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} élève(s) désactivé(s) avec succès.')
    
    @admin.action(description='Marquer comme diplômé')
    def mark_graduated(self, request, queryset):
        """Action pour diplômer les élèves"""
        updated = queryset.update(status='graduated')
        self.message_user(request, f'{updated} élève(s) diplômé(s) avec succès.')
    
    @admin.action(description='Suspendre les élèves sélectionnés')
    def mark_suspended(self, request, queryset):
        """Action pour suspendre les élèves"""
        updated = queryset.update(status='suspended')
        self.message_user(request, f'{updated} élève(s) suspendu(s) avec succès.')
