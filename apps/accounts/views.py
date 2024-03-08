from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone

from .forms import CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser, StatusUpdate, Notification
from apps.courses.models import Course, Enrollment
from .serializers import CustomUserSerializer,  UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer, StatusUpdateSerializer
from apps.courses.serializers import CourseSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# API views for user detail, registration, login, profile, password change, and notifications

# Allows users to view and update their own profile
class CustomUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Allows new users to register
class UserRegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  

# Authenticates users and returns a token for session management
class LoginAPIView(APIView):
    permission_classes = []  

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
# Provides user profile details and allows for profile updates
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
    
# Enables authenticated users to change their password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Marks a specific notification as read for the user
class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)

# Allows teachers to block students from their courses
class BlockStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, student_id):
        if request.user.user_type != 'teacher':
            return Response({'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        student = get_object_or_404(CustomUser, id=student_id)
        courses = Course.objects.filter(teacher=request.user)
        
        for course in courses:
            Enrollment.objects.filter(student=student, course=course).delete()

        return Response({'message': f'{student.username} has been blocked and unenrolled from all your courses.'}, status=status.HTTP_200_OK)
    
# Allows users to post status updates    
class StatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user automatically to the current user
            status_update = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom permission to restrict object deletion    
class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can delete any objects
        if request.user.is_staff:
            return True
        # Only owners are allowed to delete their objects
        return obj.user == request.user
    
# Allows users to delete their own status updates or admins to delete any
class StatusUpdateDeleteAPIView(DestroyAPIView):
    queryset = StatusUpdate.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

# Lists courses a user is enrolled in
class UserEnrolledCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        enrollments = Enrollment.objects.filter(student_id=request.user.id)
        course_ids = enrollments.values_list('course', flat=True)
        courses = Course.objects.filter(id__in=course_ids)
        
        if not courses:
            return Response({'message': 'You are not enrolled in any courses.'}, status=404)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
#-------------------------------------------------------------    
# Traditional Django views for user and profile management
    
# Handles user registration using a custom form
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Displays a welcome message post-registration
def welcome(request):
     return render(request, 'accounts/welcome.html')

# Handles the login process
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(2592000)  
            else:
                request.session.set_expiry(0)  

            return redirect('home')
        else:
            
            pass

    return render(request, 'login.html')

# Allows users to view and edit their profile
@login_required
def profile(request):
    edit_mode = request.GET.get('edit', '0') == '1'
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'edit_mode': edit_mode})

# Enables users to change their password through a form
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            
            update_session_auth_hash(request, user)
            logout(request)   
            messages.success(request, 'Your password was successfully updated! Please log in again.')
            return redirect('login')   
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
        })

# Handles profile editing
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assuming you have a profile view to redirect to
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

# Logs out the user
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")  # Optional: add a success message
    return redirect('home')  # Redirect to homepage or login page

# Displays the user's homepage with relevant information
@login_required
def user_home(request, username):
    user = get_object_or_404(CustomUser, username=username)
    status_updates = StatusUpdate.objects.filter(user=user).order_by('-created_at')

 
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

# Allows users to create a new status update
def status_update(request):
    if request.method == "POST":
 
        text = request.POST.get('status', '')
        if text:
            StatusUpdate.objects.create(user=request.user, text=text)
            messages.success(request, "Status updated successfully.")
        else:
            messages.error(request, "Status cannot be empty.")
    return redirect('/')

# Marks a notification as read
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
 
    return redirect("/courses" + notification.url)

# Blocks a student from the teacher's courses
@login_required
def block_student(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
 
    if request.user.user_type == 'teacher':
 
        courses = Course.objects.filter(teacher=request.user)
 
        for course in courses:
            Enrollment.objects.filter(student=student, course=course).delete()
        messages.success(request, f'{student.username} has been blocked and unenrolled from all your courses.')
    else:
        messages.error(request, 'You do not have permission to perform this action.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))