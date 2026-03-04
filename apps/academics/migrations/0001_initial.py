# Generated migration for Academics app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2035)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_years', to='accounts.school')),
            ],
            options={
                'verbose_name': 'Academic Year',
                'verbose_name_plural': 'Academic Years',
                'ordering': ['-year'],
                'unique_together': {('school', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ex: Mathématiques, Français', max_length=100)),
                ('code', models.CharField(help_text='Code unique (ex: MATH, FR)', max_length=20)),
                ('coefficient', models.FloatField(choices=[(0.5, '0.5'), (1, '1'), (1.5, '1.5'), (2, '2'), (2.5, '2.5'), (3, '3'), (3.5, '3.5'), (4, '4'), (5, '5')], default=1, help_text='Coefficient pour le calcul de moyenne')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='accounts.school')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
                'ordering': ['name'],
                'unique_together': {('school', 'code')},
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ex: 6ème A, Première S', max_length=50)),
                ('level', models.CharField(choices=[('1', 'Niveau 1 (Reception)'), ('2', 'Niveau 2'), ('3', 'Niveau 3'), ('4', 'Niveau 4'), ('5', 'Niveau 5'), ('6', 'Niveau 6'), ('7', 'Niveau 7'), ('8', 'Niveau 8'), ('9', 'Niveau 9'), ('10', 'Niveau 10 (SEC 1)'), ('11', 'Niveau 11 (SEC 2)'), ('12', 'Niveau 12 (SEC 3)')], help_text='Niveau académique', max_length=2)),
                ('room', models.CharField(blank=True, help_text='Numéro ou nom de la salle', max_length=20, null=True)),
                ('capacity', models.PositiveIntegerField(default=40, help_text='Capacité maximale', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
                ('teacher', models.CharField(blank=True, help_text='Professeur principal', max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='academics.academicyear')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='accounts.school')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
                'ordering': ['level', 'name'],
                'unique_together': {('school', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ClassSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(blank=True, help_text='Professeur de cette matière dans cette classe', max_length=100, null=True)),
                ('hours_per_week', models.PositiveIntegerField(default=1, help_text='Heures par semaine', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_subjects', to='academics.class')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_subjects', to='academics.subject')),
            ],
            options={
                'verbose_name': 'Class Subject',
                'verbose_name_plural': 'Class Subjects',
                'ordering': ['class_obj', 'subject'],
                'unique_together': {('class_obj', 'subject')},
            },
        ),
        # Create indexes
        migrations.AddIndex(
            model_name='class',
            index=models.Index(fields=['school', 'level'], name='academics_c_school_idx'),
        ),
        migrations.AddIndex(
            model_name='class',
            index=models.Index(fields=['school', 'academic_year'], name='academics_c_school_year_idx'),
        ),
        migrations.AddIndex(
            model_name='subject',
            index=models.Index(fields=['school', 'code'], name='academics_s_school_code_idx'),
        ),
        migrations.AddIndex(
            model_name='subject',
            index=models.Index(fields=['school', 'is_active'], name='academics_s_school_active_idx'),
        ),
    ]
