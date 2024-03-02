from django.urls import path
from apps.courses import views 

app_name = 'courses'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:id>/', views.course_detail, name='course_detail'),
    path('<int:id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
]
