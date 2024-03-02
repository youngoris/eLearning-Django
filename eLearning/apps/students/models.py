from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    # 可以根据需要添加更多学生特有的字段
    enrolled_courses = models.ManyToManyField('courses.Course', related_name='enrolled_students')

    def __str__(self):
        return self.user.get_full_name() or self.user.username
