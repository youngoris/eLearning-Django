# api/serializers.py
from rest_framework import serializers
from apps.accounts.models import CustomUser
from apps.courses.models import Course

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']

    # create a new user
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    # update user info
    def update(self, instance, validated_data):
        #  update user info
        instance.username = validated_data.get('username', instance.username)
      
        instance.save()
        return instance
    
# Serializer for the Course model
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

