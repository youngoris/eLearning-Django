from django.urls import path
from apps.courses import views 

# URL patterns for the traditional courses app

app_name = 'courses' # Defines the application namespace for URL names
urlpatterns = [
    path('<int:id>/', views.course_detail, name='course_detail'),    # URL pattern for accessing the detail view of a specific course using its ID
    path('<int:id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('<int:id>/edit/', views.edit_course, name='edit_course'),
    path('<int:id>/add_comment/', views.add_comment_to_course, name='add_comment'),
    path('add/', views.add_course, name='add_course'),
    # URL for listing all courses belonging to a specific category, using the category's ID
    path('categories/<int:category_id>/', views.courses_by_category, name='category_courses'),
    path('upload-file/', views.upload_teacher_file, name='upload_teacher_file_url_name'),
]


