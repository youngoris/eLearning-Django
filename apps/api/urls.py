from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CourseViewSet

# URL patterns for the API
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)), # Include the router URLs
]