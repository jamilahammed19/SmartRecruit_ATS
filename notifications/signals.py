from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification
from .tasks import send_resilient_email

# Trigger 1: Listens to the User table
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        if not instance.is_staff and not instance.is_superuser:
            subject = "Welcome to SmartRecruit!"
            message = f"Hello {instance.username},\n\nYour candidate profile has been successfully created. You can now apply for jobs, track your pipeline status, and communicate with HR directly through our portal.\n\nBest of luck,\nThe SmartRecruit Team"
            
            # 'instance' is the User. We get the email directly.
            send_resilient_email.delay(subject, message, [instance.email])


# Trigger 2: Listens to the Notification table
@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        subject = f"SmartRecruit Update: {instance.title}"
        message = f"Hello {instance.user.username},\n\nYou have a new update regarding your application:\n\n{instance.message}\n\nPlease log in to your dashboard to view more details.\n\nThank you,\nSmartRecruit HR"
        
        # 'instance' is the Notification. We must cross over to the User table to get the email.
        send_resilient_email.delay(subject, message, [instance.user.email])