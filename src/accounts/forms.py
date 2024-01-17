from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator


class CustomPasswordValidator:
    @staticmethod
    def validate(password):
        errors = []

        # Use the individual validators directly
        for validator in [MinimumLengthValidator(), CommonPasswordValidator(), NumericPasswordValidator()]:
            try:
                validator.validate(password)
            except ValidationError as error:
                errors.extend(error.messages)

        # Add your custom validation logic here
        # Example: Password must contain at least one uppercase letter
        if not any(char.isupper() for char in password):
            errors.append("The password must contain at least one uppercase letter.")

        if errors:
            raise ValidationError(errors)


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Create a username (only letters and numbers)', 'required': 'True'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'required': 'True'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'required': 'True'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'required': 'True'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'required': 'True'}),
        validators=[CustomPasswordValidator.validate]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'required': 'True'}),
        validators=[CustomPasswordValidator.validate]
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
class PaymentForm(forms.Form):
    card_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your card number', 'required': 'True'}))
    expiration_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter expiration date (MM/YY)', 'required': 'True'}))
    security_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter security code', 'required': 'True'}))

    class Meta:
        fields = ('card_number', 'expiration_date', 'security_code')

