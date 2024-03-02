# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    real_name = models.CharField(max_length=100, verbose_name=_("Real Name"))
    birth_date = models.DateField(verbose_name=_("Birth Date"))
    country = models.CharField(max_length=50, verbose_name=_("Country"))
