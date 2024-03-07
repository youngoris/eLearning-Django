from django.urls import path
from .views import  CustomUserDetailView, UserRegisterAPIView, LoginAPIView, UserProfileView, ChangePasswordView, BlockStudentAPIView, StatusUpdateAPIView, MarkNotificationAsReadAPIView, StatusUpdateDeleteAPIView, UserEnrolledCoursesAPIView


app_name = 'accounts-api'

urlpatterns = [
    path('user/', CustomUserDetailView.as_view(), name='custom_user_detail'),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('notifications/<int:notification_id>/read/', MarkNotificationAsReadAPIView.as_view(), name='mark-notification-read'),
    path('block-student/<int:student_id>/', BlockStudentAPIView.as_view(), name='block-student'),
    path('status/', StatusUpdateAPIView.as_view(), name='status-update'),
    path('status/delete/<int:id>/', StatusUpdateDeleteAPIView.as_view(), name='delete-status-update'),
    path('enrolled/', UserEnrolledCoursesAPIView.as_view(), name='user-enrolled-courses'),


]