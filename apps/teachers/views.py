from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher
from apps.courses.forms import CourseForm  # 假设您有一个表单处理课程信息
from apps.courses.models import Course  # 确保导入路径正确

@login_required
def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

@login_required
def add_course(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher  # 假设Course模型中有指向Teacher的外键
            course.save()
            return redirect('some-view')  # 重定向到适当的视图
    else:
        form = CourseForm()
    return render(request, 'teachers/add_course.html', {'form': form, 'teacher': teacher})
