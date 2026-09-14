from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import smtplib

# This decorator transforms our standard Python function into an asynchronous background task.
# autoretry_for: Tells Celery to catch SMTP (email server) connection crashes.
# retry_backoff: If it fails, wait 1s, then 2s, 4s, 8s, etc., before trying again.
# max_retries: It will keep attempting for hours until the email server is back online.
@shared_task(
    bind=True, 
    autoretry_for=(smtplib.SMTPException, Exception), 
    retry_backoff=True, 
    max_retries=48
)
def send_resilient_email(self, subject, message, recipient_list):
    """
    Sends an email asynchronously. If the SMTP server is down, Celery catches 
    the error and automatically places the email back in the Redis queue to try later.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        
        # fail_silently=False ensures the task actually throws a hard error if it fails.
        # If we set this to True, Celery would think it succeeded and delete the task forever!
        fail_silently=False, 
    )