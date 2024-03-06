from django.shortcuts import render, redirect
from apps.courses.models import Course
from apps.accounts.models import CustomUser
from .models import ChatRoom
from django.http import JsonResponse



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


def chat_room(request, room_name):
    if not room_name:
        # 如果没有指定聊天室，重定向到默认的公共聊天室
        room_name = 'Public Room'
    room, created = ChatRoom.objects.get_or_create(title=room_name)
    rooms = ChatRoom.objects.filter(members=request.user).exclude(title='Public Room')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'rooms': rooms
    })


def create_chat_room(request):
    # 假设前端通过POST请求发送聊天室名称
    room_name = request.POST.get('room_name')
    room, created = ChatRoom.objects.get_or_create(title=room_name)
    if created:
        # 聊天室创建成功
        return JsonResponse({'status': 'success', 'room_name': room.title})
    else:
        # 聊天室已存在
        return JsonResponse({'status': 'exists', 'room_name': room.title})
    
def chat_view(request, room_name=None):
    if not room_name:
        return redirect('chat_view', room_name='Public Room')