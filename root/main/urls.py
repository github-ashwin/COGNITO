from django.urls import path
from .views import *


urlpatterns = [
    path('login/',loginpage,name='login'),
    path('',home,name='home'),
    path('register/',registerpage,name='register'),
    path('room/<int:pk>/',room,name='room'),
    path('profile/<int:pk>/',user_profile,name='user_profile'),
    path('update_user/',update_user,name='update_user'),
    path('createroom/',create_room,name='create_room'),
    path('updateroom/<int:pk>/',update_room,name='update_room'),
    path('deleteroom/<int:pk>/',delete_room,name='delete_room'),
    path('deletemessage/<int:pk>/',delete_message,name='delete_message'),
    path('logout/',logout_user,name='logout')
]
