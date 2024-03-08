from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
 
    enrolled_courses = models.ManyToManyField('courses.Course', related_name='enrolled_students')

    def __str__(self):
        return self.user.get_full_name() or self.user.username
