from django.urls import path
from apps.courses import views 


app_name = 'courses'
urlpatterns = [
    path('<int:id>/', views.course_detail, name='course_detail'),
    path('<int:id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('<int:id>/edit/', views.edit_course, name='edit_course'),
    path('<int:id>/add_comment/', views.add_comment_to_course, name='add_comment'),
    path('add/', views.add_course, name='add_course'),
    path('categories/<int:category_id>/', views.courses_by_category, name='category_courses'),
    path('upload-file/', views.upload_teacher_file, name='upload_teacher_file_url_name'),

]
