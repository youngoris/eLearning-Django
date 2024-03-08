from django.db import models
from apps.accounts.models import CustomUser  # import custom user model
from django.contrib.auth.models import User  # unused import, consider removing if not used elsewhere
from django.db.models import Avg  # used for calculating average rating
from django.conf import settings  # for referencing settings like AUTH_USER_MODEL

# defines a category model for courses, including a unique name and optional description
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Description")

    # returns the name of the category when the model instance is printed
    def __str__(self):
        return self.name

# defines a subcategory model, linked to Category, includes name and optional description
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Parent Category")
    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    description = models.TextField(blank=True, verbose_name="Description")

    # returns the full path (category > subcategory name) when the model instance is printed
    def __str__(self):
        return f"{self.category.name} > {self.name}"

# defines a language model for courses with a unique name
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Language Name")

    # returns the name of the language when the model instance is printed
    def __str__(self):
        return self.name

# defines the main course model including details like title, description, teacher, etc.
class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_courses', verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', verbose_name="Category", default=1)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name="Language")
    cover = models.ImageField(upload_to='courses/covers/', blank=True, null=True, verbose_name="Course Cover")
    videos = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name="Course Videos")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    # returns the course title when the model instance is printed
    def __str__(self):
        return self.title
    
    # method to calculate and return the average rating of the course based on comments
    def average_rating(self):
        return self.comments.aggregate(Avg('rating'))['rating__avg'] or 0

# defines a model for course materials with a link to the course and an optional file
class Material(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='courses/materials/', blank=True, null=True, verbose_name="Course Material")

    # returns the material name, defaults to "Material" if name is not provided
    def __str__(self):
        return self.name or "Material"

# defines a model for course comments, including the course, user, comment text, and an optional rating
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name="Course")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    text = models.TextField(verbose_name="Comment Text")
    rating = models.IntegerField(verbose_name="Rating", default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    # returns a string indicating which user commented on which course
    def __str__(self):
        return f"Feedback by {self.user.username} on {self.course.title}"

# defines a model for tracking enrollments, including the student, course, enrollment date, grade, and status
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    date_enrolled = models.DateField(auto_now_add=True, verbose_name="Date Enrolled")
    grade = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')], default='active', verbose_name="Status")

    # returns a string indicating which student enrolled in which course
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
# defines a model for teacher-uploaded files, not directly related to courses
class TeacherFile(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='teacher_files/', blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # returns a string indicating who uploaded the file and when
    def __str__(self):
        return f"File uploaded by {self.teacher.username} on {self.uploaded_at}"
