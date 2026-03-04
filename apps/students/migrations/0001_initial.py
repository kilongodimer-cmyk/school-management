# Generated migration for Students app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),  # Dépend de l'app accounts
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('student_id', models.CharField(max_length=50, unique=True, verbose_name='Numéro d\'élève')),
                ('grade', models.CharField(help_text='Ex: 6ème A, Terminale S, etc.', max_length=50, verbose_name='Classe/Niveau')),
                ('date_of_birth', models.DateField(verbose_name='Date de naissance')),
                ('gender', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')], default='M', max_length=1, verbose_name='Genre')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adresse')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville')),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Code postal')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Pays')),
                ('parent_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nom du parent/tuteur')),
                ('parent_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone du parent')),
                ('parent_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email du parent')),
                ('enrollment_date', models.DateField(auto_now_add=True, verbose_name='Date d\'inscription')),
                ('gpa', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Moyenne générale')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='students/photos/', verbose_name='Photo')),
                ('status', models.CharField(choices=[('active', 'Actif'), ('inactive', 'Inactif'), ('graduated', 'Diplômé'), ('suspended', 'Suspendu')], default='active', max_length=20, verbose_name='Statut')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='accounts.school', verbose_name='École')),
            ],
            options={
                'verbose_name': 'Élève',
                'verbose_name_plural': 'Élèves',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['school', 'grade'], name='students_st_school_grade_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['school', 'status'], name='students_st_school_status_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['student_id'], name='students_st_student_id_idx'),
        ),
    ]
