from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('lead', 'Lead'),
        ('message', 'Message'),
        ('announcement', 'annonce'),
        # Add other types as needed
    )

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    redirect_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'
