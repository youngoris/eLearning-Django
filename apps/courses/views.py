from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CourseForm, MaterialFormSet, TeacherFileForm
from .models import Course, Enrollment, Comment, Category
from apps.accounts.models import CustomUser, Notification
from .serializers import CourseSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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



@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    average_rating = course.average_rating()  # 调用模型中的方法计算平均评分
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    has_rated = Comment.objects.filter(course=course, user=request.user).exists()
    comments = course.comments.order_by('-created_at')
    materials = course.materials.all()

    # 假设推荐逻辑是基于同一分类下的其他课程
    recommended_courses = Course.objects.filter(category=course.category).exclude(id=id)[:3]  # 获取除当前课程外的三个同分类的课程

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'average_rating': average_rating,
        'has_rated': has_rated,
        'recommended_courses': recommended_courses,
        'comments': comments,
        'materials': materials,
  # 将推荐课程加入上下文
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
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
def add_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.teacher = request.user  # 确保这里将当前用户设置为新课程的教师
            new_course.save()  # 必须先保存Course，才能创建与之关联的Material实例

                        # 向所有学生发送通知
            students = CustomUser.objects.filter(user_type='student')
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    title="New Course Available",
                    message=f"A new course '{new_course.title}' is now available. Check it out!",
                    url= str(new_course.id),
                )
            
            # 初始化MaterialFormSet与新创建的Course实例
            material_formset = MaterialFormSet(request.POST, request.FILES, instance=new_course)
            
            if material_formset.is_valid():
                material_formset.save()  # 保存材料
                return redirect('courses:course_detail', id=new_course.id)  # 重定向到新课程的详情页面

    else:
        course_form = CourseForm()
        material_formset = MaterialFormSet()
    return render(request, 'courses/add_course.html', {'form': course_form, 'material_formset': material_formset})



@login_required
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


@login_required
def add_comment_to_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # 假设你有一个 Comment 模型，你需要根据你的具体模型来创建评论
        Comment.objects.create(course=course, user=request.user, text=comment_text)
        messages.success(request, 'Your comment has been added.')

    Notification.objects.create(
        recipient=course.teacher,
        title="New Comment in Your Course",
        message=f"A new comment has been posted in your course '{course.title}'.",
        url=f"/{course.id}" + "/#comments", 
    )

    return redirect('courses:course_detail', id=id)

def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    context = {
        'courses': courses,
        'category_name': category.name,  # 假设Category模型有一个name字段
    }
    return render(request, 'courses/category_courses.html', context)


@login_required
def upload_teacher_file(request):
    if request.method == 'POST':
        form = TeacherFileForm(request.POST, request.FILES)
        if form.is_valid():
            teacher_file = form.save(commit=False)
            teacher_file.teacher = request.user
            teacher_file.save()
            # 返回JSON响应
            return JsonResponse({
                'success': True,
                'file_url': teacher_file.file.url,
                'file_name': teacher_file.file.name,
            })
        else:
            return JsonResponse({'success': False})
    # 对于GET请求，仍然渲染页面
    return render(request, 'main/user_home.html')