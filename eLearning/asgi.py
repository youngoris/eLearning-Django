"""
ASGI config for eLearning project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

# set default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eLearning.settings')
django_asgi_app = get_asgi_application()

# import the AuthMiddlewareStack and URLRouter from channels to handle WebSocket connections
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.main.routing

# define the application for the ASGI protocol
application = ProtocolTypeRouter({
    "http": django_asgi_app,  
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.main.routing.websocket_urlpatterns
        )
    ),
})
