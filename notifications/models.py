from django.db import models
from core.models import TimeStampedModel

# Create your models here.

TYPE_CHOICES = [
    ('interview', 'Interview'),
    ('application', 'Application'),
    ('general', 'General'),
]

class Notification(TimeStampedModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='general')

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"