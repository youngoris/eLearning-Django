from django.urls import path
from apps.courses import views 

app_name = 'courses'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:id>/', views.course_detail, name='course_detail'),
    path('<int:id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('course/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/add_comment/', views.add_comment_to_course, name='add_comment'),
    path('categories/<int:category_id>/', views.category_courses, name='category_courses'),

]
