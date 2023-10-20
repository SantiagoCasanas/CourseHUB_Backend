import json
import pdb
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")

    def test_user_list_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_view(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "test full name",
            "password": "newpassword"
        }
        response = self.client.post(reverse("user-create"), data, format="json")
        #pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_retrieve_update_destroy_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_view(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(reverse("user-login"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout_view(self):
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        data = {"refresh_token": refresh_token}
        response = self.client.post(reverse("user-logout"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
