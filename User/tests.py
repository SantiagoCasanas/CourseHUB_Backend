from django.test import TestCase
import pytest
from django.core.exceptions import ValidationError
from .models import User

@pytest.mark.django_db
def test_user_password_min_length():
    # Prueba que la validación de la longitud mínima de la contraseña funcione
    with pytest.raises(ValidationError):
        user = User(username="testuser", email="test@example.com", full_name="Test User", password="short")

@pytest.mark.django_db
def test_user_creation():
    # Prueba la creación de un usuario
    user = User.objects.create(username="testuser", email="test@example.com", full_name="Test User", password="securepass")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.check_password("securepass")  # Asegura que la contraseña sea correcta

@pytest.mark.django_db
def test_user_str_representation():
    # Prueba la representación de cadena del usuario
    user = User(username="testuser", email="test@example.com", full_name="Test User", password="securepass")
    assert str(user) == "User: testuser"

