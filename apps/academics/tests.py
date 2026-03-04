from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta
from apps.accounts.models import School
from .models import AcademicYear, Class, Subject, ClassSubject

User = get_user_model()


class AcademicYearModelTest(TestCase):
    """Test cases for AcademicYear model"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
    
    def test_create_academic_year(self):
        """Test creating an academic year"""
        year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30),
            is_active=True
        )
        self.assertEqual(str(year), '2024 (Test School)')
        self.assertTrue(year.is_active)
    
    def test_academic_year_unique_together(self):
        """Test unique constraint on school and year"""
        AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
        
        with self.assertRaises(Exception):
            AcademicYear.objects.create(
                school=self.school,
                year=2024,
                start_date=date(2024, 8, 1),
                end_date=date(2025, 7, 30)
            )
    
    def test_is_current_property(self):
        """Test is_current property"""
        year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
        )
        self.assertTrue(year.is_current)


class ClassModelTest(TestCase):
    """Test cases for Class model"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
        self.year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
    
    def test_create_class(self):
        """Test creating a class"""
        class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            capacity=40,
            academic_year=self.year
        )
        self.assertEqual(str(class_obj), '6ème A (Test School)')
        self.assertEqual(class_obj.student_count, 0)
        self.assertEqual(class_obj.available_spots, 40)
        self.assertFalse(class_obj.is_full)
    
    def test_class_full_name_property(self):
        """Test full_name property"""
        class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        self.assertEqual(class_obj.full_name, '6ème A - Niveau 6')
    
    def test_class_unique_together(self):
        """Test unique constraint on school and name"""
        Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        
        with self.assertRaises(Exception):
            Class.objects.create(
                school=self.school,
                name='6ème A',
                level='6',
                academic_year=self.year
            )


class SubjectModelTest(TestCase):
    """Test cases for Subject model"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
    
    def test_create_subject(self):
        """Test creating a subject"""
        subject = Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH',
            coefficient=3
        )
        self.assertEqual(str(subject), 'Mathématiques (MATH) - Coeff: 3')
        self.assertTrue(subject.is_active)
    
    def test_subject_unique_together(self):
        """Test unique constraint on school and code"""
        Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH',
            coefficient=3
        )
        
        with self.assertRaises(Exception):
            Subject.objects.create(
                school=self.school,
                name='Maths',
                code='MATH',
                coefficient=2
            )
    
    def test_subject_inactive(self):
        """Test creating inactive subject"""
        subject = Subject.objects.create(
            school=self.school,
            name='Chimie',
            code='CHEM',
            is_active=False
        )
        self.assertFalse(subject.is_active)


class ClassSubjectModelTest(TestCase):
    """Test cases for ClassSubject model"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
        self.year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
        self.class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        self.subject = Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH'
        )
    
    def test_create_class_subject(self):
        """Test creating a class subject link"""
        cs = ClassSubject.objects.create(
            class_obj=self.class_obj,
            subject=self.subject,
            teacher='Jean Dupont',
            hours_per_week=3
        )
        self.assertEqual(str(cs), '6ème A - Mathématiques')
        self.assertTrue(cs.is_active)


class ClassCRUDTest(TestCase):
    """Test CRUD operations for classes"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
        self.year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
        self.user = User.objects.create_user(
            email='director@test.com',
            password='test123',
            school=self.school,
            role='director'
        )
        self.client = Client()
        self.client.login(email='director@test.com', password='test123')
    
    def test_class_list_view(self):
        """Test class list view"""
        Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        response = self.client.get(reverse('academics:class_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('classes', response.context)
    
    def test_class_create(self):
        """Test creating a class via view"""
        response = self.client.post(
            reverse('academics:class_create'),
            {
                'name': '6ème B',
                'level': '6',
                'capacity': 35,
                'academic_year': self.year.id,
                'teacher': 'Marie Dupont'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Class.objects.filter(name='6ème B').exists())
    
    def test_class_detail_view(self):
        """Test class detail view"""
        class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        response = self.client.get(
            reverse('academics:class_detail', args=[class_obj.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['class'], class_obj)
    
    def test_class_update(self):
        """Test updating a class"""
        class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        response = self.client.post(
            reverse('academics:class_update', args=[class_obj.id]),
            {
                'name': '6ème A Updated',
                'level': '6',
                'capacity': 40,
                'academic_year': self.year.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        class_obj.refresh_from_db()
        self.assertEqual(class_obj.name, '6ème A Updated')
    
    def test_class_delete(self):
        """Test deleting a class"""
        class_obj = Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        response = self.client.post(
            reverse('academics:class_delete', args=[class_obj.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Class.objects.filter(id=class_obj.id).exists())


class SubjectCRUDTest(TestCase):
    """Test CRUD operations for subjects"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
        self.user = User.objects.create_user(
            email='director@test.com',
            password='test123',
            school=self.school,
            role='director'
        )
        self.client = Client()
        self.client.login(email='director@test.com', password='test123')
    
    def test_subject_list_view(self):
        """Test subject list view"""
        Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH'
        )
        response = self.client.get(reverse('academics:subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('subjects', response.context)
    
    def test_subject_create(self):
        """Test creating a subject"""
        response = self.client.post(
            reverse('academics:subject_create'),
            {
                'name': 'Français',
                'code': 'FR',
                'coefficient': 2,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subject.objects.filter(code='FR').exists())
    
    def test_subject_detail_view(self):
        """Test subject detail view"""
        subject = Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH'
        )
        response = self.client.get(
            reverse('academics:subject_detail', args=[subject.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['subject'], subject)
    
    def test_subject_update(self):
        """Test updating a subject"""
        subject = Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH',
            coefficient=2
        )
        response = self.client.post(
            reverse('academics:subject_update', args=[subject.id]),
            {
                'name': 'Mathématiques Avancées',
                'code': 'MATH',
                'coefficient': 3,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 302)
        subject.refresh_from_db()
        self.assertEqual(subject.coefficient, 3)


class SchoolDataIsolationTest(TestCase):
    """Test data isolation by school"""
    
    def setUp(self):
        """Set up test data"""
        self.school1 = School.objects.create(
            name='School 1',
            code='SCH001'
        )
        self.school2 = School.objects.create(
            name='School 2',
            code='SCH002'
        )
        self.year1 = AcademicYear.objects.create(
            school=self.school1,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
        self.class1 = Class.objects.create(
            school=self.school1,
            name='6ème A',
            level='6',
            academic_year=self.year1
        )
        self.class2 = Class.objects.create(
            school=self.school2,
            name='6ème A',
            level='6'
        )
        
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='test123',
            school=self.school1,
            role='director'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='test123',
            school=self.school2,
            role='director'
        )
    
    def test_class_isolation(self):
        """Test that users only see their school's classes"""
        self.client = Client()
        self.client.login(email='user1@test.com', password='test123')
        
        response = self.client.get(reverse('academics:class_list'))
        classes = response.context['classes']
        
        # User1 should only see class1
        self.assertIn(self.class1, classes)
        self.assertNotIn(self.class2, classes)
    
    def test_subject_isolation(self):
        """Test that users only see their school's subjects"""
        Subject.objects.create(
            school=self.school1,
            name='Mathématiques',
            code='MATH'
        )
        Subject.objects.create(
            school=self.school2,
            name='Français',
            code='FR'
        )
        
        self.client = Client()
        self.client.login(email='user1@test.com', password='test123')
        
        response = self.client.get(reverse('academics:subject_list'))
        subjects = response.context['subjects']
        
        # User1 should only see MATH
        self.assertEqual(subjects.count(), 1)
        self.assertEqual(subjects[0].code, 'MATH')


class SearchAndFilterTest(TestCase):
    """Test search and filter functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.school = School.objects.create(
            name='Test School',
            code='TEST001'
        )
        self.year = AcademicYear.objects.create(
            school=self.school,
            year=2024,
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30)
        )
        
        # Create multiple classes
        Class.objects.create(
            school=self.school,
            name='6ème A',
            level='6',
            academic_year=self.year
        )
        Class.objects.create(
            school=self.school,
            name='6ème B',
            level='6',
            academic_year=self.year
        )
        Class.objects.create(
            school=self.school,
            name='5ème A',
            level='5',
            academic_year=self.year
        )
        
        # Create subjects
        Subject.objects.create(
            school=self.school,
            name='Mathématiques',
            code='MATH',
            coefficient=2
        )
        Subject.objects.create(
            school=self.school,
            name='Français',
            code='FR',
            coefficient=3
        )
        
        self.user = User.objects.create_user(
            email='user@test.com',
            password='test123',
            school=self.school,
            role='director'
        )
        self.client = Client()
        self.client.login(email='user@test.com', password='test123')
    
    def test_class_search(self):
        """Test searching classes"""
        response = self.client.get(
            reverse('academics:class_list') + '?search=6ème'
        )
        classes = response.context['classes']
        self.assertEqual(classes.count(), 2)
    
    def test_class_filter_by_level(self):
        """Test filtering classes by level"""
        response = self.client.get(
            reverse('academics:class_list') + '?level=6'
        )
        classes = response.context['classes']
        self.assertEqual(classes.count(), 2)
    
    def test_subject_search(self):
        """Test searching subjects"""
        response = self.client.get(
            reverse('academics:subject_list') + '?search=math'
        )
        subjects = response.context['subjects']
        self.assertEqual(subjects.count(), 1)
    
    def test_subject_filter_by_coefficient(self):
        """Test filtering subjects by coefficient"""
        response = self.client.get(
            reverse('academics:subject_list') + '?coefficient=2'
        )
        subjects = response.context['subjects']
        self.assertEqual(subjects.count(), 1)
