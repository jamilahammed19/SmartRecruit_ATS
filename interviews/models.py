from django.db import models
from core.models import TimeStampedModel
from applications.models import Application

# Create your models here.

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]


class Interview(TimeStampedModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(default=30, help_text="Duration of the interview in minutes")
    location = models.CharField(max_length=255, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True, help_text="Link for virtual interviews")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.application.candidate} - {self.scheduled_time}"


class RescheduleRequest(TimeStampedModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    requested_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reschedule Request for {self.interview.application.candidate} - {self.requested_time}"
    

