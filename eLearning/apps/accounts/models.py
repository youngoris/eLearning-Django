from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # 添加用户类型的选项
    USER_TYPE_CHOICES = (
        ('student', _('Student')),
        ('teacher', _('Teacher')),
    )
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='student', verbose_name=_("User Type"))

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    real_name = models.CharField(max_length=100, blank=True, verbose_name=_("Real Name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    country = models.CharField(max_length=50, blank=True, verbose_name=_("Country"))

    def __str__(self):
        return self.username
