from django.db import models
from django.conf import settings

# Create a model for the teacher profile
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
