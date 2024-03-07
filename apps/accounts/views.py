from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone

from .forms import CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser, StatusUpdate, Notification
from apps.courses.models import Course, Enrollment
from .serializers import CustomUserSerializer,  UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token



class CustomUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)  # partial=True 允许部分更新
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # 允许任何用户注册


class LoginAPIView(APIView):
    permission_classes = []  # 允许任何人访问，即使是未认证的用户

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEnrolledCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        enrollments = Enrollment.objects.filter(student=user)
        courses = Course.objects.filter(enrollments__in=enrollments)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


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

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    # 重定向到通知关联的URL或某个默认页面
    return redirect("/courses" + notification.url)

@login_required
def block_student(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    # 确保当前登录的用户是教师
    if request.user.user_type == 'teacher':
        # 获取当前教师的所有课程
        courses = Course.objects.filter(teacher=request.user)
        # 对于每个课程，取消学生的注册
        for course in courses:
            Enrollment.objects.filter(student=student, course=course).delete()
        messages.success(request, f'{student.username} has been blocked and unenrolled from all your courses.')
    else:
        messages.error(request, 'You do not have permission to perform this action.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))