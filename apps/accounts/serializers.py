from rest_framework import serializers
from .models import CustomUser, StatusUpdate

from django.contrib.auth import get_user_model  # Fetch the custom user model
from django.contrib.auth.hashers import make_password  # For hashing passwords
from django.contrib.auth.password_validation import validate_password  # For validating passwords
from django.core.exceptions import ValidationError

User = get_user_model()  # Assign the custom user model to 'User'

# Serializer for the custom user model, specifying fields to be serialized
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_type', 'email',  'avatar', 'real_name',  'birth_date' ,'country']

# Serializer for user registration, includes password handling
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Password field, write-only to ensure it's not returned by the API

    class Meta:
        model = User
        fields = ('username', 'user_type', 'email',  'avatar', 'real_name',  'birth_date' ,'country')
    
    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)

# Serializer for viewing and updating user profiles, marking username as read-only
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'user_type', 'email',  'avatar', 'real_name',  'birth_date' ,'country')
        read_only_fields = ('username',) 

# Serializer for changing user passwords, includes custom validation
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        # Validate that the old password is correct
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        # Validate the new password against Django's password policy
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        # Update user's password
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

# Serializer for status updates, with user and created_at as read-only fields
class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = ['text']
        read_only_fields = ['user', 'created_at']
