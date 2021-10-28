from django.db import models
from accounts.models import Profile
# Create your models here.


class Room(models.Model):
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin')
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    sender = models.CharField(max_length=100)

    def __str__(self):
        return self.message

