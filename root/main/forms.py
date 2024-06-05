from django.forms import ModelForm
from .models import *


class room_form(ModelForm): # django form for creating room
    class Meta:
        model = Room
        fields = '__all__'