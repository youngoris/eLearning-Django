from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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

@login_required
def profile(request):
    context = {
        'user': request.user,
        'is_student': request.user.user_type == 'student',
        'is_teacher': request.user.user_type == 'teacher',
    }
    return render(request, 'accounts/profile.html', context)