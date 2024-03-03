from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.courses.models import Course, Enrollment

def home(request):
    courses = Course.objects.all()[:5]  # 举例，获取最新的5门课程
    context = {'courses': courses}

    if request.user.is_authenticated:
        if hasattr(request.user, 'teacher_profile'):
            # 为教师用户准备的上下文
            teacher_courses = request.user.authored_courses.all()
            context.update({'teacher_courses': teacher_courses})
        elif hasattr(request.user, 'student_profile'):
            # 为学生用户准备的上下文
            student_profile = request.user.student_profile
            student_user = student_profile.user  # 获取 CustomUser 实例
            student_enrollments = Enrollment.objects.filter(student=student_user)
            context.update({'student_enrollments': student_enrollments})


    return render(request, 'main/home.html', context)

