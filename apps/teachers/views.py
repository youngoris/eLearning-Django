from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.courses.forms import CourseForm
from apps.courses.models import Course

def is_teacher(user):
    return user.is_authenticated and user.user_type == 'teacher'

@login_required
@user_passes_test(is_teacher)
def add_course(request):
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


def teacher_detail(request, id):

    return render(request, 'teachers/teacher_detail.html', {})