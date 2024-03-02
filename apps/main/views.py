# apps/main/views.py
from django.shortcuts import render
from apps.courses.models import Course  # 确保路径正确

def home(request):
    courses = Course.objects.all().order_by('-id')[:5]
    return render(request, 'main/home.html', {'courses': courses})
