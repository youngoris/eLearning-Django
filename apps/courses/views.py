# Import necessary Django and REST framework components
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, MaterialFormSet, TeacherFileForm
from .models import Course, Enrollment, Comment, Category
from apps.accounts.models import CustomUser, Notification
from .serializers import CourseSerializer, CategorySerializer, LanguageSerializer, TeacherSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Class-based views for CRUD operations on courses using generic views for simplicity and reduced code
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# APIViews for listing categories, languages, and teachers; allows for fetching data in JSON format
class CategoryListView(APIView):
    # Return a list of all categories
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class LanguageListView(APIView):
    # Return a list of all languages
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
    
class TeacherListView(APIView):
    # Return a list of all teachers
    def get(self, request):
        teachers = CustomUser.objects.filter(is_teacher=True)  # Assumes is_teacher field exists
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

# Custom view for filtering courses based on category, language, or teacher
class CourseFilterView(APIView):
    def get(self, request):
        # Filter courses dynamically based on query parameters
        courses = Course.objects.all()
        for key in ['category', 'language', 'teacher']:
            param = request.query_params.get(key, None)
            if param is not None:
                courses = courses.filter(**{f"{key}_id": param})

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

# ---------------------------------------------------
# Standard Django views for course details, enrollment, and course management, using forms and models
    
@login_required
# Display details for a single course, including enrollment and rating status
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    average_rating = course.average_rating()   
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    has_rated = Comment.objects.filter(course=course, user=request.user).exists()
    comments = course.comments.order_by('-created_at')
    materials = course.materials.all()
 
    recommended_courses = Course.objects.filter(category=course.category).exclude(id=id)[:3]   

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'average_rating': average_rating,
        'has_rated': has_rated,
        'recommended_courses': recommended_courses,
        'comments': comments,
        'materials': materials,
 
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
# Handle enrollment to a course, including success and error messages
def enroll_in_course(request, id):
    course = get_object_or_404(Course, id=id)
    student = request.user  

    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, "You have been enrolled in the course successfully.")

        Notification.objects.create(
        recipient=course.teacher,
        title="New Student Enrolled",
        message=f"A new student enrolled in your course '{course.title}'.",
        url=f"/{course.id}", 
    )

    return redirect('courses:course_detail', id=id)

@login_required
# View for adding a new course, handling POST for form submission and file uploads
def add_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.teacher = request.user   
            new_course.save()   

 
            students = CustomUser.objects.filter(user_type='student')
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    title="New Course Available",
                    message=f"A new course '{new_course.title}' is now available. Check it out!",
                    url= str(new_course.id),
                )
 
            material_formset = MaterialFormSet(request.POST, request.FILES, instance=new_course)
            
            if material_formset.is_valid():
                material_formset.save()  
                return redirect('courses:course_detail', id=new_course.id)  

    else:
        course_form = CourseForm()
        material_formset = MaterialFormSet()
    return render(request, 'courses/add_course.html', {'form': course_form, 'material_formset': material_formset})

@login_required
# View for editing an existing course, handling form and material formset
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        material_formset = MaterialFormSet(request.POST, request.FILES, instance=course)
        if form.is_valid() and material_formset.is_valid():
            form.save()
            material_formset.save()
            return redirect('courses:course_detail', id=course.id)
    else:
        form = CourseForm(instance=course)
        material_formset = MaterialFormSet(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'material_formset': material_formset, 'course': course})

# Display a list of featured courses, simple query with limit
def featured_courses(request):
    featured_courses=[]
    featured_courses = Course.objects.all()[:5]   
    context = {'courses': featured_courses}
    return render(request, 'main/home.html', context)

# Allow authenticated users to add comments to a course and notify the course teacher
@login_required
def add_comment_to_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
 
        Comment.objects.create(course=course, user=request.user, text=comment_text)
        messages.success(request, 'Your comment has been added.')

    Notification.objects.create(
        recipient=course.teacher,
        title="New Comment in Your Course",
        message=f"A new comment has been posted in your course '{course.title}'.",
        url=f"/{course.id}" + "/#comments", 
    )
    return redirect('courses:course_detail', id=id)

# Display courses filtered by a specific category
def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    context = {
        'courses': courses,
        'category_name': category.name,   
    }
    return render(request, 'courses/category_courses.html', context)

# Handle file upload by teachers, responding with JSON for AJAX requests
@login_required
def upload_teacher_file(request):
    if request.method == 'POST':
        form = TeacherFileForm(request.POST, request.FILES)
        if form.is_valid():
            teacher_file = form.save(commit=False)
            teacher_file.teacher = request.user
            teacher_file.save()
 
            return JsonResponse({
                'success': True,
                'file_url': teacher_file.file.url,
                'file_name': teacher_file.file.name,
            })
        else:
            return JsonResponse({'success': False})
 
    return render(request, 'main/user_home.html')