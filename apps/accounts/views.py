from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


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
    edit_mode = request.GET.get('edit', '0') == '1'
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # 重定向到不含查询参数的profile页面，以退出编辑模式
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'edit_mode': edit_mode})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # 从表单获取记住我复选框的值

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(2592000)  # 设置会话过期时间为30天
            else:
                request.session.set_expiry(0)  # 会话在浏览器关闭时过期

            return redirect('home')
        else:
            # 处理登录失败的情况
            pass

    # 如果是GET请求或者登录失败，渲染登录表单
    return render(request, 'login.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 更新session以防用户被登出，但是我们接下来会立即登出用户
            update_session_auth_hash(request, user)
            logout(request)  # 登出用户
            messages.success(request, 'Your password was successfully updated! Please log in again.')
            return redirect('login')  # 重定向到登录页面
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
        })

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assuming you have a profile view to redirect to
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")  # Optional: add a success message
    return redirect('home')  # Redirect to homepage or login page