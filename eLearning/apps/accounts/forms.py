from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_type', 'username', 'email', 'avatar',  'real_name', 'birth_date', 'country')  # 添加或移除字段以匹配你的CustomUser模型
