# apps/courses/forms.py
from django import forms
from .models import Course

# Define a form for the Course model
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description','teacher', 'start_date', 'end_date']
