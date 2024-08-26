from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_view(request):
    # Get unread notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    
    # Mark all as read
    notifications.update(is_read=True)
    
    # Context to pass to the template
    context = {
        'notifications': notifications
    }
    
    return render(request, 'notifications.html', context)


def create_notification(user, notification_type, **kwargs):
    if notification_type == 'lead':
        lead = kwargs.get('lead')
        message = f"New lead added: {lead.first_name} {lead.last_name} at {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    elif notification_type == 'message':
        sender = kwargs.get('sender')
        message = f"New message from {sender.username}"
    elif notification_type == 'file':
        file_name = kwargs.get('file_name')
        message = f"New file uploaded: {file_name}"
    else:
        message = "You have a new notification"

    Notification.objects.create(
        user=user,
        message=message,
        type=notification_type,
        is_read=False
    )
