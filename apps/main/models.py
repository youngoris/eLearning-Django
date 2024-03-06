from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')

    def __str__(self):
        return self.title

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."
