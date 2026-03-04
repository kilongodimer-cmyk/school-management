"""
Commande personnalisée pour créer une école avec ses utilisateurs
Usage: python manage.py create_school_with_users
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.accounts.models import School, CustomUser


class Command(BaseCommand):
    """Commande pour créer une école complète avec utilisateurs"""
    
    help = "Crée une école avec ses utilisateurs (directeur, enseignants, etc.)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='École Nouvelle',
            help='Nom de l\'école'
        )
        parser.add_argument(
            '--code',
            type=str,
            default='EC001',
            help='Code de l\'école'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='contact@ecole.com',
            help='Email de l\'école'
        )
        parser.add_argument(
            '--director',
            type=str,
            default='Jean Dupont',
            help='Nom du directeur'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Exécute la commande"""
        
        name = options['name']
        code = options['code']
        email = options['email']
        director_name = options['director']
        
        try:
            # Créer l'école
            school, created = School.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'email': email,
                    'director_name': director_name,
                    'max_students': 500,
                    'max_teachers': 50,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ École créée: {school.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'ⓘ École existe déjà: {school.name}')
                )
            
            # Créer le directeur
            director_user, _ = CustomUser.objects.get_or_create(
                username=f'director_{code.lower()}',
                defaults={
                    'email': f'director@{code.lower()}.com',
                    'first_name': director_name.split()[0],
                    'last_name': director_name.split()[-1] if len(director_name.split()) > 1 else 'Director',
                    'school': school,
                    'role': 'director',
                    'is_verified': True,
                }
            )
            
            if _ is True:
                director_user.set_password('director123')
                director_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Directeur créé: {director_user.get_full_name()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'ⓘ Directeur existe déjà')
                )
            
            # Créer quelques enseignants
            teachers = [
                ('Jean', 'Martin', 'teacher1'),
                ('Marie', 'Bernard', 'teacher2'),
                ('Paul', 'Dubois', 'teacher3'),
            ]
            
            for first_name, last_name, username in teachers:
                user, created = CustomUser.objects.get_or_create(
                    username=f'{username}_{code.lower()}',
                    defaults={
                        'email': f'{username}@{code.lower()}.com',
                        'first_name': first_name,
                        'last_name': last_name,
                        'school': school,
                        'role': 'teacher',
                        'is_verified': True,
                    }
                )
                
                if created:
                    user.set_password('teacher123')
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Enseignant créé: {user.get_full_name()}')
                    )
            
            # Créer un comptable
            accountant, created = CustomUser.objects.get_or_create(
                username=f'accountant_{code.lower()}',
                defaults={
                    'email': f'accountant@{code.lower()}.com',
                    'first_name': 'Alice',
                    'last_name': 'Comptable',
                    'school': school,
                    'role': 'accountant',
                    'is_verified': True,
                }
            )
            
            if created:
                accountant.set_password('accountant123')
                accountant.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Comptable créé: {accountant.get_full_name()}')
                )
            
            # Résumé
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('✓ École créée avec succès!'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(f'\nÉcole: {school.name} ({school.code})')
            self.stdout.write(f'Utilisateurs créés: {school.users.count()}')
            self.stdout.write(f'\nIdentifiants de test:')
            self.stdout.write(f'  Directeur: director_{code.lower()} / director123')
            self.stdout.write(f'  Enseignant: teacher1_{code.lower()} / teacher123')
            self.stdout.write(f'  Comptable: accountant_{code.lower()} / accountant123')
            
        except Exception as e:
            raise CommandError(f'Erreur lors de la création: {str(e)}')
