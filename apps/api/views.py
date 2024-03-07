from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import CustomUser
from apps.courses.models import Course
from .serializers import UserSerializer, CourseSerializer

class UserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer