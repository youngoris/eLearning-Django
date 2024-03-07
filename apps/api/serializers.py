# api/serializers.py
from rest_framework import serializers
from apps.accounts.models import CustomUser
from apps.courses.models import Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
