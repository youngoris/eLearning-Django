from django.urls import path
from .views import  CustomUserDetailView, UserRegisterAPIView, LoginAPIView, UserProfileView, ChangePasswordView



app_name = 'accounts-api'

urlpatterns = [
    path('user/', CustomUserDetailView.as_view(), name='custom_user_detail'),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]