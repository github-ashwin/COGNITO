from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('room/<int:pk>/',room,name='room'),
    path('createroom/',create_room,name='create_room'),
    path('updateroom/<int:pk>/',update_room,name='update_room'),
    path('deleteroom/<int:pk>/',delete_room,name='delete_room'),
]
