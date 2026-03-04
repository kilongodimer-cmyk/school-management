from django.contrib import admin
from django.utils.html import format_html
from .models import AcademicYear, Class, Subject, ClassSubject, Term, Grade


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    """Admin for Academic Year"""
    list_display = ('year_badge', 'school_link', 'start_date', 'end_date', 'is_active')
    list_filter = ('school', 'year', 'is_active', 'created_at')
    search_fields = ('year', 'school__name')
    readonly_fields = ('created_at', 'updated_at', 'school_link')
    
    fieldsets = (
        ('Académique', {
            'fields': ('school', 'year', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def year_badge(self, obj):
        """Show year as badge"""
        color = '#28a745' if obj.is_active else '#6c757d'
        status = '✓ Actif' if obj.is_active else 'Inactif'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            f'{obj.year} ({status})'
        )
    year_badge.short_description = 'Année'
    
    def school_link(self, obj):
        """Link to school"""
        if obj.school:
            return format_html(
                '<a href="/admin/accounts/school/{}/change/">{}</a>',
                obj.school.pk,
                obj.school.name
            )
        return '-'
    school_link.short_description = 'École'


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Admin for Classes"""
    list_display = ('name_badge', 'level_badge', 'school_link', 'capacity_bar', 'teacher', 'academic_year')
    list_filter = ('school', 'level', 'academic_year', 'created_at')
    search_fields = ('name', 'school__name', 'teacher', 'level')
    readonly_fields = ('created_at', 'updated_at', 'school_link', 'student_count_display')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('school', 'name', 'level', 'room')
        }),
        ('Académique', {
            'fields': ('academic_year', 'teacher')
        }),
        ('Capacité', {
            'fields': ('capacity', 'student_count_display')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_badge(self, obj):
        """Show class name as badge"""
        return format_html(
            '<span style="background-color: #667eea; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.name
        )
    name_badge.short_description = 'Classe'
    
    def level_badge(self, obj):
        """Show level as colored badge"""
        levels = {
            '1': '#667eea', '2': '#667eea', '3': '#667eea',
            '4': '#667eea', '5': '#667eea', '6': '#667eea',
            '7': '#764ba2', '8': '#764ba2', '9': '#764ba2',
            '10': '#f093fb', '11': '#f093fb', '12': '#f093fb',
        }
        color = levels.get(obj.level, '#667eea')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">Niv. {}</span>',
            color,
            obj.level
        )
    level_badge.short_description = 'Niveau'
    
    def capacity_bar(self, obj):
        """Show capacity as progress bar"""
        percentage = (obj.student_count / obj.capacity * 100) if obj.capacity > 0 else 0
        color = '#28a745' if percentage < 80 else '#ffc107' if percentage < 100 else '#dc3545'
        return format_html(
            '<div style="width: 150px; background-color: #e9ecef; border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; background-color: {}; height: 20px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">'
            '{}/{}</div></div>',
            percentage, color, obj.student_count, obj.capacity
        )
    capacity_bar.short_description = 'Capacité'
    
    def student_count_display(self, obj):
        """Display student count"""
        return f"{obj.student_count} élèves"
    student_count_display.short_description = 'Nombre d\'élèves'
    
    def school_link(self, obj):
        """Link to school"""
        if obj.school:
            return format_html(
                '<a href="/admin/accounts/school/{}/change/">{}</a>',
                obj.school.pk,
                obj.school.name
            )
        return '-'
    school_link.short_description = 'École'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin for Subjects"""
    list_display = ('name_badge', 'code_badge', 'coefficient_badge', 'school_link', 'status_badge')
    list_filter = ('school', 'coefficient', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'school__name')
    readonly_fields = ('created_at', 'updated_at', 'school_link', 'class_count_display')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('school', 'name', 'code')
        }),
        ('Académique', {
            'fields': ('coefficient', 'is_active')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('class_count_display',),
            'classes': ('collapse',)
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_badge(self, obj):
        """Show subject name as badge"""
        return format_html(
            '<span style="background-color: #764ba2; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.name
        )
    name_badge.short_description = 'Matière'
    
    def code_badge(self, obj):
        """Show code as badge"""
        return format_html(
            '<span style="background-color: #667eea; color: white; padding: 5px 7px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.code
        )
    code_badge.short_description = 'Code'
    
    def coefficient_badge(self, obj):
        """Show coefficient as badge"""
        return format_html(
            '<span style="background-color: #f093fb; color: white; padding: 5px 10px; border-radius: 3px;">Coeff: {}</span>',
            obj.coefficient
        )
    coefficient_badge.short_description = 'Coefficient'
    
    def status_badge(self, obj):
        """Show status as badge"""
        color = '#28a745' if obj.is_active else '#6c757d'
        status = '✓ Actif' if obj.is_active else 'Inactif'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Statut'
    
    def school_link(self, obj):
        """Link to school"""
        if obj.school:
            return format_html(
                '<a href="/admin/accounts/school/{}/change/">{}</a>',
                obj.school.pk,
                obj.school.name
            )
        return '-'
    school_link.short_description = 'École'
    
    def class_count_display(self, obj):
        """Display number of classes"""
        count = obj.class_subjects.count()
        return f"{count} classe{'s' if count != 1 else ''}"
    class_count_display.short_description = 'Nombre de classes'


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    """Admin for Class Subjects"""
    list_display = ('class_name_badge', 'subject_badge', 'teacher', 'hours_badge', 'status_badge')
    list_filter = ('is_active', 'hours_per_week', 'created_at')
    search_fields = ('class_obj__name', 'subject__name', 'teacher')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Classe et Matière', {
            'fields': ('class_obj', 'subject')
        }),
        ('Professeur', {
            'fields': ('teacher',)
        }),
        ('Planning', {
            'fields': ('hours_per_week', 'is_active')
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def class_name_badge(self, obj):
        """Show class name as badge"""
        return format_html(
            '<span style="background-color: #667eea; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.class_obj.name
        )
    class_name_badge.short_description = 'Classe'
    
    def subject_badge(self, obj):
        """Show subject as badge"""
        return format_html(
            '<span style="background-color: #764ba2; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.subject.name
        )
    subject_badge.short_description = 'Matière'
    
    def hours_badge(self, obj):
        """Show hours per week as badge"""
        return format_html(
            '<span style="background-color: #f093fb; color: white; padding: 5px 10px; border-radius: 3px;">{} h</span>',
            obj.hours_per_week
        )
    hours_badge.short_description = 'Heures/semaine'
    
    def status_badge(self, obj):
        """Show status as badge"""
        color = '#28a745' if obj.is_active else '#6c757d'
        status = '✓ Actif' if obj.is_active else 'Inactif'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Statut'


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """Admin for Terms"""
    list_display = ('term_badge', 'school_link', 'academic_year', 'start_date', 'end_date', 'is_active')
    list_filter = ('school', 'academic_year', 'term_number', 'is_active')
    search_fields = ('name', 'school__name')
    readonly_fields = ('created_at', 'updated_at', 'school_link')
    
    fieldsets = (
        ('Informations', {
            'fields': ('school', 'academic_year', 'term_number', 'name')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def term_badge(self, obj):
        """Show term as badge"""
        colors = {'1': '#667eea', '2': '#764ba2', '3': '#f093fb'}
        color = colors.get(obj.term_number, '#667eea')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.name
        )
    term_badge.short_description = 'Trimestre'
    
    def school_link(self, obj):
        """Link to school"""
        if obj.school:
            return format_html(
                '<a href="/admin/accounts/school/{}/change/">{}</a>',
                obj.school.pk,
                obj.school.name
            )
        return '-'
    school_link.short_description = 'École'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin for Grades"""
    list_display = ('student_name', 'subject_badge', 'term_badge', 'score_badge', 'rating_badge', 'school_link')
    list_filter = ('school', 'term', 'subject', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name', 'student__student_id')
    readonly_fields = ('created_at', 'updated_at', 'school_link', 'rating_display')
    
    fieldsets = (
        ('Élève et Matière', {
            'fields': ('school', 'student', 'subject', 'term')
        }),
        ('Note', {
            'fields': ('score', 'rating_display')
        }),
        ('Commentaires', {
            'fields': ('comments',),
            'classes': ('collapse',)
        }),
        ('Système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_name(self, obj):
        """Show student full name as link"""
        return format_html(
            '<a href="{}"><strong>{}</strong></a>',
            f'/admin/students/student/{obj.student.pk}/change/',
            obj.student.full_name
        )
    student_name.short_description = 'Élève'
    
    def subject_badge(self, obj):
        """Show subject as badge"""
        return format_html(
            '<span style="background-color: #764ba2; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.subject.code
        )
    subject_badge.short_description = 'Matière'
    
    def term_badge(self, obj):
        """Show term as badge"""
        return format_html(
            '<span style="background-color: #667eea; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.term.name
        )
    term_badge.short_description = 'Trimestre'
    
    def score_badge(self, obj):
        """Show score with color coding"""
        color = 'success' if obj.score >= 16 else 'info' if obj.score >= 12 else 'warning' if obj.score >= 10 else 'danger'
        return format_html(
            '<span class="badge bg-{}" style="font-size: 14px;">{}/20</span>',
            color,
            obj.score
        )
    score_badge.short_description = 'Note'
    
    def rating_badge(self, obj):
        """Show rating"""
        rating_colors = {
            'Excellent': '#28a745',
            'Très Bien': '#28a745',
            'Bien': '#17a2b8',
            'Assez Bien': '#17a2b8',
            'Passable': '#ffc107',
            'Faible': '#dc3545',
        }
        color = rating_colors.get(obj.rating, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.rating
        )
    rating_badge.short_description = 'Appréciation'
    
    def rating_display(self, obj):
        """Display rating"""
        return obj.rating
    rating_display.short_description = 'Rating'
    
    def school_link(self, obj):
        """Link to school"""
        if obj.school:
            return format_html(
                '<a href="/admin/accounts/school/{}/change/">{}</a>',
                obj.school.pk,
                obj.school.name
            )
        return '-'
    school_link.short_description = 'École'
