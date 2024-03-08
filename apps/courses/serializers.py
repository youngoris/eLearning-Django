from rest_framework import serializers
from .models import Course, Category, Language
from apps.accounts.models import CustomUser

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # specifies the model to be serialized
        fields = ['id', 'name', 'description']  # specifies which fields to include in the serialization

# Serializer for the Language model
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language  # specifies the model to be serialized
        fields = ['id', 'name']  # specifies which fields to include in the serialization

# Serializer for the Course model, includes nested serializers for category and language
class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # nested serializer for the category, read-only to avoid update issues
    language = LanguageSerializer(read_only=True)  # nested serializer for the language, read-only to avoid update issues
    teacher = serializers.SlugRelatedField(slug_field='username', read_only=True)  # shows the teacher's username instead of the ID

    class Meta:
        model = Course  # specifies the model to be serialized
        fields = ['title', 'description', 'teacher', 'category', 'language', 'cover', 'videos', 'start_date', 'end_date', 'created_at']  # specifies which fields to include

    # custom method to get the average rating for the course
    def get_average_rating(self, obj):
        return obj.average_rating()

# Redefinition of CategorySerializer to include all fields from the model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # specifies the model to be serialized
        fields = '__all__'  # includes all fields in the model in the serialization

# Redefinition of LanguageSerializer to include all fields from the model
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language  # specifies the model to be serialized
        fields = '__all__'  # includes all fields in the model in the serialization

# Serializer for the CustomUser model, targeting teacher data specifically
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # specifies the model to be serialized
        fields = ['id', 'username', 'real_name', 'email']  # specifies which fields to include, focusing on identification and contact information
