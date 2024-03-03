from django.db import models
from apps.accounts.models import CustomUser
from django.contrib.auth.models import User
from django.db.models import Avg



from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Parent Category")
    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return f"{self.category.name} > {self.name}"   

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Language Name")

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_courses', verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', verbose_name="Category", default=1)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name="Language")
    cover = models.ImageField(upload_to='courses/covers/', blank=True, null=True, verbose_name="Course Cover")
    videos = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name="Course Videos")
    materials = models.FileField(upload_to='courses/materials/', blank=True, null=True, verbose_name="Course Materials")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.title
    
    def average_rating(self):
        return self.comments.aggregate(Avg('rating'))['rating__avg'] or 0

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name="Course")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    text = models.TextField(verbose_name="Comment Text")
    rating = models.IntegerField(verbose_name="Rating", default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.course.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    date_enrolled = models.DateField(auto_now_add=True, verbose_name="Date Enrolled")
    grade = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')], default='active', verbose_name="Status")


    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
