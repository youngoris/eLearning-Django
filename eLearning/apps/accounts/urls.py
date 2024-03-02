from django.urls import path
from .views import register, welcome, profile, change_password, edit_profile
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('welcome/', welcome, name='welcome'),
    path('profile/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'), 
    path('edit_profile/', edit_profile, name='edit_profile'),

]