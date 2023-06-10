from django.test import TestCase
from apps.users.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

class ModelTestCase(TestCase):
    
    def setUp(self):
        self.pseudonym = "hari"
        self.user = User(pseudonym=self.pseudonym)

    def test_model_can_create_user(self):
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username":"dk_hari", 
                            "password":"hello@1234",
                            "password2":"hello@1234",
                            "email":"dh@gmail.com", 
                            "pseudonym":"deekshi_hari"
                            }
        self.response = self.client.post(reverse('auth_register'), self.user_data, format="json")

    def test_api_can_create_User(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)