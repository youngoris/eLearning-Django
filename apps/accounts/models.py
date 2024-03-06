from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.templatetags.static import static



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', _('Student')),
        ('teacher', _('Teacher')),
    )
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='student', verbose_name=_("User Type"))
    avatar = models.ImageField(upload_to='user/avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    real_name = models.CharField(max_length=100, blank=True, verbose_name=_("Real Name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    country = models.CharField(max_length=50, blank=True, verbose_name=_("Country"))

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static('admin/img/avatar.svg')

    def __str__(self):
        return self.username


class StatusUpdate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()  # 确保有这个字段
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status update by {self.user.username} on {self.created_at}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url = models.CharField(max_length=255, default='/')

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"