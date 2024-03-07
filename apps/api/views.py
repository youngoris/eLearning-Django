from rest_framework import viewsets
from apps.accounts.models import CustomUser
from apps.courses.models import Course
from .serializers import UserSerializer, CourseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer