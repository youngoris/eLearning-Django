from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_type', 'username', 'email', 'avatar',  'real_name', 'birth_date', 'country')   

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'real_name', 'birth_date', 'country', 'avatar']