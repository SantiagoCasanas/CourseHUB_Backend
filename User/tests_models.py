from django.test import TestCase
from .models import User
from django.forms import ValidationError

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            full_name="Test User"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="adminpassword",
            full_name="Admin User"
        )
        self.assertEqual(user.username, "adminuser")
        self.assertEqual(user.email, "adminuser@example.com")
        self.assertTrue(user.check_password("adminpassword"))
        self.assertEqual(user.full_name, "Admin User")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_case_fail_with_empty_username(self):
        with self.assertRaises(ValidationError):
            user = User(username="",
                email="testuser@example.com",
                password="testpassword",
                full_name="Test User")
            user.full_clean()
    
    def test_case_fail_with_empty_email(self):
        with self.assertRaises(ValidationError):
            user = User(username="testuser",
                email="",
                password="testpassword",
                full_name="Test User")
            user.full_clean()
    
    def test_case_fail_with_wrong_password(self):
        with self.assertRaises(ValidationError):
            user = User(username="testuser",
                email="testuser@example.com",
                password="123456",
                full_name="Test User")
            user.full_clean()

    