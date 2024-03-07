from rest_framework import serializers
from .models import Course, Category, Language
from apps.accounts.models import CustomUser

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    teacher = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher', 'category', 'language', 
                  'cover', 'videos', 'start_date', 'end_date', 'created_at']

    
    def get_average_rating(self, obj):
        return obj.average_rating()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'real_name', 'email'] 