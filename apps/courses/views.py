from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, Comment 


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    average_rating = course.average_rating()  # 调用模型中的方法计算平均评分
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    has_rated = Comment.objects.filter(course=course, user=request.user).exists()

    # 假设推荐逻辑是基于同一分类下的其他课程
    recommended_courses = Course.objects.filter(category=course.category).exclude(id=id)[:3]  # 获取除当前课程外的三个同分类的课程

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'average_rating': average_rating,
        'has_rated': has_rated,
        'recommended_courses': recommended_courses,  # 将推荐课程加入上下文
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

    return redirect('courses:course_detail', id=id)


@login_required
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})



@login_required
def add_comment_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # 假设你有一个 Comment 模型，你需要根据你的具体模型来创建评论
        Comment.objects.create(course=course, user=request.user, text=comment_text)
        messages.success(request, 'Your comment has been added.')
    return redirect('courses:course_detail', id=course_id)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 11)]),
            'text': forms.Textarea(attrs={'placeholder': 'Add a comment...'})
        }