from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import CustomUser, StatusUpdate, Notification
from apps.courses.models import Course, Enrollment
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def welcome(request):
    # 处理视图逻辑
    return render(request, 'accounts/welcome.html')

@login_required
def profile(request):
    edit_mode = request.GET.get('edit', '0') == '1'
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # 重定向到不含查询参数的profile页面，以退出编辑模式
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'edit_mode': edit_mode})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # 从表单获取记住我复选框的值

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(2592000)  # 设置会话过期时间为30天
            else:
                request.session.set_expiry(0)  # 会话在浏览器关闭时过期

            return redirect('home')
        else:
            # 处理登录失败的情况
            pass

    # 如果是GET请求或者登录失败，渲染登录表单
    return render(request, 'login.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 更新session以防用户被登出，但是我们接下来会立即登出用户
            update_session_auth_hash(request, user)
            logout(request)  # 登出用户
            messages.success(request, 'Your password was successfully updated! Please log in again.')
            return redirect('login')  # 重定向到登录页面
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
        })

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assuming you have a profile view to redirect to
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")  # Optional: add a success message
    return redirect('home')  # Redirect to homepage or login page

@login_required
def user_home(request, username):
    user = get_object_or_404(CustomUser, username=username)
    status_updates = StatusUpdate.objects.filter(user=user).order_by('-created_at')

    # 初始化变量，以避免UnboundLocalError
    my_courses = []
    available_courses = []
    my_students = []
    upcoming_deadlines = []

    if user.user_type == 'student':
        enrollments = Enrollment.objects.filter(student=user)
        my_courses = [enrollment.course for enrollment in enrollments]
        upcoming_deadlines = Course.objects.filter(
            enrollments__in=enrollments,
            end_date__gt=timezone.now()
        ).distinct().order_by('end_date')[:5]
        available_courses = Course.objects.exclude(id__in=[course.id for course in my_courses])

    elif user.user_type == 'teacher':
        my_courses = user.authored_courses.all()
        my_students = CustomUser.objects.filter(
            enrollments__course__teacher=user
        ).distinct()

    context = {
        'user_profile': user,
        'status_updates': status_updates,
        'my_courses': my_courses,
        'upcoming_deadlines': upcoming_deadlines if user.user_type == 'student' else None,
        'available_courses': available_courses if user.user_type == 'student' else None,
        'my_students': my_students if user.user_type == 'teacher' else None,
    }

    return render(request, 'accounts/user_home.html', context)

def status_update(request):
    if request.method == "POST":
        # 处理状态更新逻辑
        text = request.POST.get('status', '')
        if text:
            StatusUpdate.objects.create(user=request.user, text=text)
            messages.success(request, "Status updated successfully.")
        else:
            messages.error(request, "Status cannot be empty.")
    return redirect('/')


def send_notification_to_teacher(student, course):
    # 假设 course 有一个 teacher 属性指向教师
    Notification.objects.create(
        recipient=course.teacher,
        title="New student enrolled",
        message=f"{student.username} has enrolled in your course {course.title}."
    )

def send_notification_to_students(course):
    for student in course.students.all():
        Notification.objects.create(
            recipient=student,
            title="Course updated",
            message=f"{course.title} has been updated. Check out the new content!"
        )