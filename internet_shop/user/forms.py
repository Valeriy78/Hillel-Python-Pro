"""
User application forms
"""

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import UserModel


class RegisterForm(forms.ModelForm):
    """Form for new user registration"""

    class Meta:
        model = UserModel
        fields = "username", "email", "password"
        widgets = {
            "password": forms.PasswordInput
        }

    password2 = forms.CharField(max_length=32, label="Password again", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserModel.objects.get(username=username)
            raise ValidationError("User with this username already exists")
        except UserModel.DoesNotExist:
            return username

    def clean(self):
        password1 = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise ValidationError("passwords mismatch")

    def create_user(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        UserModel.objects.create_user(username, email, password)


class LoginForm(forms.ModelForm):
    """Login user form"""

    class Meta:
        model = UserModel
        fields = "username", "password"
        widgets = {
            "password": forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError("Invalid username or password")


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""

    class Meta:
        model = UserModel
        fields = "first_name", "last_name", "email"

    def get_items(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }


