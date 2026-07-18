from django.db import models
from core.models import TimeStampedModel

# Create your models here.

class Job(TimeStampedModel):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=100, help_text="e.g., Engineering, Marketing, Sales")
    description = models.TextField()
    ai_short_description = models.TextField(blank=True, null=True, help_text="AI-generated short description of the job")
    requirements = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('processing', 'In Processing Stage'), ('completed','Completed')], default='open')


