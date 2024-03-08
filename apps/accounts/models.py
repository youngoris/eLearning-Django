from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for internationalization
from django.conf import settings
from django.templatetags.static import static  # Allows for static file referencing

# Extend the default User model to include additional fields like user type, avatar, etc.
class CustomUser(AbstractUser):
    # Define user type choices and their display strings
    USER_TYPE_CHOICES = (
        ('student', _('Student')),
        ('teacher', _('Teacher')),
    )
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='student', verbose_name=_("User Type"))
    avatar = models.ImageField(upload_to='user/avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    real_name = models.CharField(max_length=100, blank=True, verbose_name=_("Real Name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    country = models.CharField(max_length=50, blank=True, verbose_name=_("Country"))

    # Returns the URL for the user's avatar or a default if none is set
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static('admin/img/avatar.svg')

    # String representation of the CustomUser model, using the username
    def __str__(self):
        return self.username

# Model to record status updates by users
class StatusUpdate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the CustomUser model
    text = models.TextField()  # Text content of the status update
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the status is created

    # String representation of the StatusUpdate model, showing the user and creation time
    def __str__(self):
        return f"Status update by {self.user.username} on {self.created_at}"

# Model for notifications sent to users
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')  # The notification recipient
    title = models.CharField(max_length=255)  # Notification title
    message = models.TextField()  # Notification message body
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of notification creation
    read = models.BooleanField(default=False)  # Boolean field to track if the notification has been read
    url = models.CharField(max_length=255, default='/')  # URL for the notification to link to, if any

    # String representation of the Notification model, showing the recipient and title
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
