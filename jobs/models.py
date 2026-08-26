from django.db import models
from core.models import TimeStampedModel

# Create your models here.
STATUS_CHOICES = [
    ('open', 'Open'), 
    ('processing', 'In Processing Stage'), 
    ('completed','Completed')
]


class Job(TimeStampedModel):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    description = models.TextField()
    ai_short_description = models.TextField(blank=True, null=True)
    requirements = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')


class AIInterviewQuestion(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)


