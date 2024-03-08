
from django.urls import path
from apps.courses.views import  CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView, CategoryListView, LanguageListView, CourseFilterView, TeacherListView

# URL patterns for the courses API

app_name = 'courses-api'

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/new/', CourseCreateView.as_view(), name='course-create'),
    path('courses/update/<int:pk>/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),
    path('courses/categories/<int:pk>/', CategoryListView.as_view(), name='category-list'),
    path('courses/languages/<int:pk>/', LanguageListView.as_view(), name='language-list'),
    path('courses/teachers/<int:pk>/', TeacherListView.as_view(), name='teacher-list'),
]

