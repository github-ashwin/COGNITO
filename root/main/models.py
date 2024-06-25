from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg") 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#Topic model to categorize rooms
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Room model representing a discussion room
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Host user, nullable
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # Topic, nullable
    name = models.CharField(max_length=200)  # Room name
    description = models.TextField(null=True, blank=True)  # Room description, optional
    participants = models.ManyToManyField(User, related_name='participants', blank=True)  # Room participants, optional
    updated = models.DateTimeField(auto_now=True)  # Timestamp of the last update
    created = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    class Meta:
        ordering = ['-updated', '-created']  # Order by last updated and created date

    def __str__(self):
        return self.name

# Message model representing a message in a room
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who posted the message
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Room where the message was posted
    body = models.TextField()  # Message content
    updated = models.DateTimeField(auto_now=True)  # Timestamp of the last update
    created = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    class Meta:
        ordering = ['-updated', '-created']  # Order by last updated and created date

    def __str__(self):
        return self.body[:50]  # Return first 50 characters of the message body
