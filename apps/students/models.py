from django.db import models
from django.conf import settings

# Create a model for the student profile
class Student(models.Model):
    # Link the Student model with the User model using a one-to-one relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
 
    # Add a many-to-many relationship with the Course model to track enrolled courses
    enrolled_courses = models.ManyToManyField('courses.Course', related_name='enrolled_students')

    def __str__(self):
        return self.user.get_full_name() or self.user.username
