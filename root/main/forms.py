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


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email'] 

