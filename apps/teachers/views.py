from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.courses.forms import CourseForm
from apps.courses.models import Course

def is_teacher(user):
    return user.is_authenticated and user.user_type == 'teacher'

# View for the teacher's course list, displaying all courses for a teacher
@login_required
@user_passes_test(is_teacher)
def add_course(request):
    # If the form has been submitted...
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            # Redirect to a new URL:
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'teachers/add_course.html', {'form': form})

# View for the teacher's course list, displaying all courses for a teacher
def teacher_detail(request, id):

    return render(request, 'teachers/teacher_detail.html', {})