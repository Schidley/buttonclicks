# clickapp/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserPreference

class UserPreferenceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserPreference.objects.create(user=self.user)

    def test_user_preference_creation(self):
        # Ensure UserPreference is created when the user is created
        user_preference = UserPreference.objects.get(user=self.user)
        self.assertIsNotNone(user_preference)
        self.assertEqual(user_preference.button_text, 'Click Me!')

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_preference = UserPreference.objects.create(user=self.user)

    def test_login_view(self):
        # Ensure the login view works and creates a UserPreference if it doesn't exist
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        user_preference = UserPreference.objects.get(user=self.user)
        self.assertIsNotNone(user_preference)

    def test_login_view_user_preference_creation(self):
        # Delete the UserPreference and ensure it is created upon login
        self.user_preference.delete()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        user_preference = UserPreference.objects.get(user=self.user)
        self.assertIsNotNone(user_preference)
