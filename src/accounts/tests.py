from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignUpForm

class SignUpFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test invalid data (e.g., missing required fields)
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)