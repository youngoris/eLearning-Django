
from django.urls import path
from apps.courses import views 

app_name = 'courses-api'
urlpatterns = [

    path('user-courses/', views.UserEnrolledCoursesAPIView.as_view(), name='user-enrolled-courses'),

]