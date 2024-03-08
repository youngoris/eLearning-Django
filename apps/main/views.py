from django.shortcuts import render, redirect
from apps.courses.models import Course
from apps.accounts.models import CustomUser
from .models import ChatRoom
from django.http import JsonResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

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
        return redirect('user_home', username=request.user.username)  
 
    return render(request, 'main/home.html')


def chat_room(request, room_name):
    if not room_name:
 
        room_name = 'Public Room'
    room, created = ChatRoom.objects.get_or_create(title=room_name)
    rooms = ChatRoom.objects.filter(members=request.user).exclude(title='Public Room')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'rooms': rooms
    })


def create_chat_room(request):
 
    room_name = request.POST.get('room_name')
    room, created = ChatRoom.objects.get_or_create(title=room_name)
    if created:
     
        return JsonResponse({'status': 'success', 'room_name': room.title})
    else:
   
        return JsonResponse({'status': 'exists', 'room_name': room.title})
    
def chat_view(request, room_name=None):
    if not room_name:
        return redirect('chat_view', room_name='Public Room')
    

# def send_chat_message(room_name, message, user):
#     channel_layer = get_channel_layer()
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间戳
#     async_to_sync(channel_layer.group_send)(
#         room_name,
#         {
#             "type": "chat_message",
#             "message": message,
#             "username": user.username,
#             "avatar_url": user.get_avatar_url(),  # 使用用户的get_avatar_url方法获取头像URL
#             "timestamp": now,  # 发送当前时间戳
#         },
#     )