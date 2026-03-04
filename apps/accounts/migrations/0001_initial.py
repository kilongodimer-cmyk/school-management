# Generated migration for Accounts app

from django.db import migrations, models
import django.contrib.auth.models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nom complet de l\'établissement', max_length=255, unique=True, verbose_name='Nom de l\'école')),
                ('code', models.CharField(help_text='Code unique pour identifier l\'école', max_length=50, unique=True, verbose_name='Code de l\'école')),
                ('email', models.EmailField(help_text='Email principal de contact', max_length=254, unique=True, verbose_name='Email de l\'école')),
                ('phone', models.CharField(blank=True, help_text='Numéro de téléphone de l\'école', max_length=20, null=True, verbose_name='Téléphone')),
                ('address', models.TextField(blank=True, help_text='Adresse complète de l\'école', null=True, verbose_name='Adresse')),
                ('postal_code', models.CharField(blank=True, help_text='Code postal', max_length=20, null=True, verbose_name='Code postal')),
                ('city', models.CharField(blank=True, help_text='Ville', max_length=100, null=True, verbose_name='Ville')),
                ('country', models.CharField(blank=True, default='Sénégal', help_text='Pays', max_length=100, null=True, verbose_name='Pays')),
                ('website', models.URLField(blank=True, help_text='Site web de l\'école', null=True, verbose_name='Site web')),
                ('logo', models.ImageField(blank=True, help_text='Logo de l\'école', null=True, upload_to='schools/logos/', verbose_name='Logo')),
                ('description', models.TextField(blank=True, help_text='Description de l\'école', null=True, verbose_name='Description')),
                ('max_students', models.IntegerField(default=1000, help_text='Limite de la capacité de l\'école', verbose_name='Nombre maximum d\'étudiants')),
                ('max_teachers', models.IntegerField(default=100, help_text='Limite du nombre d\'enseignants', verbose_name='Nombre maximum d\'enseignants')),
                ('is_active', models.BooleanField(default=True, help_text='Indique si l\'école est active', verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
            ],
            options={
                'verbose_name': 'École',
                'verbose_name_plural': 'Écoles',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.models.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user account should be considered active. Uncheck this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('role', models.CharField(choices=[('superadmin', 'Super Admin'), ('director', 'Directeur'), ('teacher', 'Enseignant'), ('accountant', 'Comptable'), ('student', 'Étudiant'), ('parent', 'Parent')], default='student', help_text='Le rôle de l\'utilisateur dans le système', max_length=20, verbose_name='Rôle')),
                ('phone', models.CharField(blank=True, help_text='Numéro de téléphone personnel', max_length=20, null=True, verbose_name='Téléphone')),
                ('address', models.TextField(blank=True, help_text='Adresse personnelle', null=True, verbose_name='Adresse')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Pays')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Code postal')),
                ('profile_photo', models.ImageField(blank=True, help_text='Photo de profil', max_length=255, null=True, upload_to='accounts/profiles/', verbose_name='Photo de profil')),
                ('birth_date', models.DateField(blank=True, help_text='Date de naissance', null=True, verbose_name='Date de naissance')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], default='M', max_length=1, verbose_name='Sexe')),
                ('is_verified', models.BooleanField(default=False, help_text='Indique si l\'email a été vérifié', verbose_name='Email vérifié')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
                ('last_login_at', models.DateTimeField(blank=True, null=True, verbose_name='Dernière connexion')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', related_query_name='customuser', to='auth.group', verbose_name='groups')),
                ('school', models.ForeignKey(blank=True, help_text='L\'école à laquelle l\'utilisateur appartient', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='accounts.school', verbose_name='École')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='customuser', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['school', 'role'], name='accounts_cu_school_role_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['email'], name='accounts_cu_email_idx'),
        ),
    ]
