from django.forms import ModelForm
from .models import Room,User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Django form for creating and updating Room instances
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # Include all fields from the Room model
        exclude = ['host','participants'] # Excluding fields from the form


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio'] 

