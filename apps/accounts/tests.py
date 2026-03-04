"""
Tests pour l'application accounts
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import School, CustomUser


class SchoolModelTest(TestCase):
    """Tests pour le modèle School"""

    def setUp(self):
        """Configuration initiale des tests"""
        self.school = School.objects.create(
            name="École Centrale",
            code="EC001",
            email="contact@ecolecentrale.com",
            director_name="Jean Dupont",
            max_students=500,
            max_teachers=50
        )

    def test_school_creation(self):
        """Test la création d'une école"""
        self.assertEqual(self.school.name, "École Centrale")
        self.assertEqual(self.school.code, "EC001")
        self.assertTrue(self.school.is_active)

    def test_school_string_representation(self):
        """Test la représentation textuelle d'une école"""
        expected = "École Centrale (EC001)"
        self.assertEqual(str(self.school), expected)

    def test_school_unique_name(self):
        """Test que le nom de l'école est unique"""
        with self.assertRaises(Exception):
            School.objects.create(
                name="École Centrale",
                code="EC002",
                email="autre@ecole.com"
            )

    def test_school_unique_code(self):
        """Test que le code de l'école est unique"""
        with self.assertRaises(Exception):
            School.objects.create(
                name="Autre École",
                code="EC001",
                email="autre@ecole.com"
            )


class CustomUserModelTest(TestCase):
    """Tests pour le modèle CustomUser"""

    def setUp(self):
        """Configuration initiale des tests"""
        self.school = School.objects.create(
            name="École Test",
            code="ET001",
            email="test@ecole.com"
        )
        
        self.user = CustomUser.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            school=self.school,
            role='teacher'
        )

    def test_user_creation(self):
        """Test la création d'un utilisateur"""
        self.assertEqual(self.user.username, "john_doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.role, 'teacher')

    def test_user_full_name(self):
        """Test l'affichage du nom complet"""
        self.assertEqual(self.user.get_full_name(), "John Doe")

    def test_user_role_methods(self):
        """Test les méthodes de vérification de rôle"""
        self.assertTrue(self.user.is_teacher())
        self.assertFalse(self.user.is_director())
        self.assertFalse(self.user.is_student())

    def test_superadmin_user(self):
        """Test la création d'un super admin"""
        superadmin = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role='superadmin'
        )
        self.assertTrue(superadmin.is_superuser)
        self.assertTrue(superadmin.is_superadmin())

    def test_student_user(self):
        """Test la création d'un étudiant"""
        student = CustomUser.objects.create_user(
            username="student1",
            email="student@example.com",
            password="student123",
            school=self.school,
            role='student'
        )
        self.assertTrue(student.is_student())
        self.assertEqual(student.role, 'student')

    def test_director_user(self):
        """Test la création d'un directeur"""
        director = CustomUser.objects.create_user(
            username="director1",
            email="director@example.com",
            password="director123",
            school=self.school,
            role='director'
        )
        self.assertTrue(director.is_director())

    def test_accountant_user(self):
        """Test la création d'un comptable"""
        accountant = CustomUser.objects.create_user(
            username="accountant1",
            email="accountant@example.com",
            password="accountant123",
            school=self.school,
            role='accountant'
        )
        self.assertTrue(accountant.is_accountant())

    def test_parent_user(self):
        """Test la création d'un parent"""
        parent = CustomUser.objects.create_user(
            username="parent1",
            email="parent@example.com",
            password="parent123",
            school=self.school,
            role='parent'
        )
        self.assertTrue(parent.is_parent())

    def test_user_string_representation(self):
        """Test la représentation textuelle d'un utilisateur"""
        expected = "John Doe (Enseignant)"
        self.assertEqual(str(self.user), expected)

    def test_full_address_property(self):
        """Test la propriété full_address"""
        self.user.address = "123 Rue de la Paix"
        self.user.postal_code = "75000"
        self.user.city = "Paris"
        self.user.country = "France"
        self.user.save()
        
        expected = "123 Rue de la Paix, 75000, Paris, France"
        self.assertEqual(self.user.full_address, expected)

    def test_school_relationship(self):
        """Test la relation entre User et School"""
        self.assertEqual(self.user.school, self.school)
        self.assertIn(self.user, self.school.users.all())

    def test_user_without_school(self):
        """Test qu'un superadmin peut ne pas avoir d'école"""
        superadmin = CustomUser.objects.create_superuser(
            username="superadmin",
            email="superadmin@example.com",
            password="superadmin123",
            role='superadmin'
        )
        self.assertIsNone(superadmin.school)


class UserAuthenticationTest(TestCase):
    """Tests pour l'authentification des utilisateurs"""

    def setUp(self):
        """Configuration initiale"""
        self.school = School.objects.create(
            name="École Auth",
            code="EA001",
            email="auth@ecole.com"
        )
        
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            school=self.school,
            role='teacher'
        )

    def test_user_password_is_hashed(self):
        """Test que le mot de passe est hashé"""
        self.assertNotEqual(self.user.password, "testpass123")

    def test_user_password_verification(self):
        """Test la vérification du mot de passe"""
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_user_login(self):
        """Test la connexion d'un utilisateur"""
        User = get_user_model()
        user = User.objects.get(username="testuser")
        self.assertTrue(user.check_password("testpass123"))
