from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('<int:id>/', views.student_detail, name='student_detail'),
    path('<int:id>/courses/', views.student_courses, name='student_courses'),
]
