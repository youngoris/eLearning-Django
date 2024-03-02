from django.db import models
from apps.teachers.models import Teacher
from django.utils import timezone


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)  


    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateField()
    grade = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"
