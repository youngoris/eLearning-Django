from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(recipient=request.user, read=False)
        }
    return {}