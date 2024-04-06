from django import forms
from accounts.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class LoginForm(forms.Form):
    email = forms.EmailField(
        help_text="Username should have at least 10 letters",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your user name"}
        ), 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your user name"}
        ),
    )


class SignUpForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your Email Address.",
            }
        ),
    )
    username = forms.CharField(
        max_length=50,
        min_length=0,
        help_text="Username should have at least 10 letters",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your user name"}
        ),
    )
    password = forms.CharField(
        max_length=10,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your user name"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=10,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your user name"}
        ),
    )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email):
            raise forms.ValidationError("You already have an account.")
        return email
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username):
            raise forms.ValidationError("This username already exists. Please choose another username.")
        if len(username) > 10:
            raise forms.ValidationError("Username cannot be greater than 10")
        return username
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password Does not match.")
        return confirm_password


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username"]

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Password Does not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password2"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "is_admin",
            "is_active",
        ]
