from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', _('Student')),
        ('teacher', _('Teacher')),
    )
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='student', verbose_name=_("User Type"))

    avatar = models.ImageField(upload_to='static/admin/img/', blank=True, null=True, verbose_name=_("Avatar"), default='static/admin/img/avatar.svg')
    real_name = models.CharField(max_length=100, blank=True, verbose_name=_("Real Name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    country = models.CharField(max_length=50, blank=True, verbose_name=_("Country"))

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.DEFAULT_AVATAR_URL

    def __str__(self):
        return self.username
