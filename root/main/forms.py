from django.forms import ModelForm
from .models import Room
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Django form for creating and updating Room instances
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # Include all fields from the Room model
        exclude = ['host','participants'] # Excluding fields from the form


# Custom user creation form extending the default UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Require email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields to be used in the form

    # Validate that the username is unique (case insensitive)
    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    # Validate that the email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
