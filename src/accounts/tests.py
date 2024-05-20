import time
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import LoginForm, PaymentForm, SignUpForm

from django.urls import reverse
from rest_framework import status

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
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'securepassword',
            'password2': 'differentpassword',  # Mismatched password
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_email(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_fields(self):
        form_data = {
            'username': '',  # Empty username
            'first_name': '',
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_form_validation_performance(self):
        start_time = time.time()
        
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
        }

        for _ in range(1000):  # Adjust the range for desired number of iterations
            form = SignUpForm(data=form_data)
            self.assertTrue(form.is_valid())
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Form validation for 1000 iterations took {duration:.2f} seconds")

        # Assert that the duration is within an acceptable range
        self.assertLess(duration, 2, "Form validation is too slow")  # Adjust threshold as needed
    
class PaymentFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'card_number': '1234567890123456',
            'expiration_date': '12/25',
            'security_code': '123',
        }
        form = PaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with missing required fields
        form_data = {}
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('card_number', form.errors)
        self.assertIn('expiration_date', form.errors)
        self.assertIn('security_code', form.errors)

        # Test with invalid card number (less than 16 digits)
        form_data['card_number'] = 'abcdasdwa'
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test with invalid expiration date format
        form_data['expiration_date'] = '12-25'  # Incorrect format
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test with invalid security code (less than 3 digits)
        form_data['security_code'] = '12'
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
    #python manage.py test accounts
    
class LoginFormTests(TestCase):
    def test_valid_form(self):
        """Test the LoginForm with valid data."""
        form_data = {
            'username': 'validuser',
            'password': 'validpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_username(self):
        """Test the LoginForm with an empty username."""
        form_data = {
            'username': '',
            'password': 'validpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)  # Assuming the form class provides this error

    def test_form_with_empty_password(self):
        """Test the LoginForm with an empty password."""
        form_data = {
            'username': 'validuser',
            'password': '',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)  # Assuming the form class provides this error

    def test_form_with_invalid_credentials(self):
        """Optionally, test handling of invalid credentials if the form includes such validation."""
        form_data = {
            'username': 'unknown',
            'password': 'wrongpassword',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        # This would require the LoginForm to have custom validation checking credentials against the database
        self.assertIn('invalid_login', form.errors)  # Assuming an error key like this is used

    def test_form_field_requirements(self):
        """Test the LoginForm to ensure both fields are required."""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
