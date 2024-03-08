from django.urls import path
from . import views

# URL patterns for the teachers app
urlpatterns = [
    path('<int:id>/', views.teacher_detail, name='teacher_detail'),
    path('<int:id>/courses/add/', views.add_course, name='add_course'),
    path('add_course', views.add_course, name='add_course'),
]
