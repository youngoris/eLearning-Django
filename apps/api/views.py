from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import CustomUser
from apps.courses.models import Course
from .serializers import UserSerializer, CourseSerializer

# ViewSets for the User and Course models
class UserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer