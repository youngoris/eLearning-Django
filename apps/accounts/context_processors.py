from .models import Notification


# Define a context processor to make the list of unread notifications available globally to all templates
def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(recipient=request.user, read=False)
        }
    return {}