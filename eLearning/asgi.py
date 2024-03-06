"""
ASGI config for eLearning project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eLearning.settings')
django_asgi_app = get_asgi_application()

# 以下导入放置在get_asgi_application()调用之后
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.main.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # 将Django ASGI应用作为HTTP类型的协议路由
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.main.routing.websocket_urlpatterns
        )
    ),
})
