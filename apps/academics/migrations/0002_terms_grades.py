# Generated migration for Terms and Grades

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
        ('accounts', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_number', models.CharField(choices=[('1', 'Trimestre 1'), ('2', 'Trimestre 2'), ('3', 'Trimestre 3')], max_length=1)),
                ('name', models.CharField(help_text='Ex: Trimestre 1', max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='academics.academicyear')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='accounts.school')),
            ],
            options={
                'verbose_name': 'Term',
                'verbose_name_plural': 'Terms',
                'ordering': ['academic_year', 'term_number'],
                'unique_together': {('academic_year', 'term_number')},
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(help_text='Score sur 20', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='accounts.school')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='students.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='academics.subject')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='academics.term')),
            ],
            options={
                'verbose_name': 'Grade',
                'verbose_name_plural': 'Grades',
                'ordering': ['student', 'subject', 'term'],
                'unique_together': {('student', 'subject', 'term')},
            },
        ),
        # Create indexes
        migrations.AddIndex(
            model_name='grade',
            index=models.Index(fields=['student', 'term'], name='academics_g_student_term_idx'),
        ),
        migrations.AddIndex(
            model_name='grade',
            index=models.Index(fields=['school', 'term'], name='academics_g_school_term_idx'),
        ),
    ]
