from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.courses.models import Course, Enrollment


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def enroll_in_course(request, id):
    course = get_object_or_404(Course, id=id)
    student = request.user.student  # 假设用户模型有一个指向学生的一对一关系

    # 检查是否已经注册
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
    else:
        # 创建注册记录
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, "You have been enrolled in the course successfully.")

    return redirect('course_detail', id=id)  # 重定向到课程详情页面