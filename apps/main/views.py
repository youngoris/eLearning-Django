from django.shortcuts import render, redirect
from apps.courses.models import Course
from apps.accounts.models import CustomUser


def home(request):
    courses = Course.objects.all()[:5]  # 假设你只想获取最新的5门课程
    print(courses)  # 打印查询到的课程列表
    context = {'courses': courses}
    return render(request, 'main/home.html', context)


def search_results(request):
    query = request.GET.get('query', '')
    course_results = Course.objects.filter(title__icontains=query)
    user_results = CustomUser.objects.filter(username__icontains=query)
    if request.user.is_authenticated and request.user.user_type == 'teacher':
        user_results = CustomUser.objects.filter(username__icontains=query)

    context = {
        'query': query,
        'course_results': course_results,
        'user_results': user_results,
        'is_teacher': request.user.is_authenticated and request.user.user_type == 'teacher',
    }
    
    return render(request, 'main/search_results.html', context)

def homepage_view(request):
    if request.user.is_authenticated:
        return redirect('user_home', username=request.user.username)  # 假设'user_home'是用户主页的URL名称
    # 渲染网站首页模板
    return render(request, 'main/home.html')