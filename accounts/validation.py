from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User

class UserValidationMixin:
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address format")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("You already have an account.")
        
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists. Please choose another username.")
        if len(username) > 10:
            raise forms.ValidationError("Username cannot be greater than 10")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2