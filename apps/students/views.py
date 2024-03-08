from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from apps.students.models import Student
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register_student(request):
    pass

@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def student_courses(request, id):
    student = get_object_or_404(Student, pk=id)
    courses = student.enrolled_courses.all()
    return render(request, 'students/student_courses.html', {'student': student, 'courses': courses})
