from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'

    def ready(self):
        from .models import ChatRoom
        ChatRoom.objects.get_or_create(title='Public Room')
