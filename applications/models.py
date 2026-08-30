from django.db import models
from core.models import TimeStampedModel
from candidates.models import CandidateProfile
from jobs.models import Job

# Create your models here.


STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('under_review', 'Under Review'),
    ('interview_scheduled', 'Interview Scheduled'),
    ('offered', 'Offered'),
    ('rejected', 'Rejected'),
    ('hired', 'Hired'),
]

INTERVIEW_STATUS_CHOICES = [
    ('scheduled', 'Scheduled (Pending Confirmation)'),
    ('accepted', 'Accepted'),
    ('reschedule_requested', 'Reschedule Requested'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
]

class Application(TimeStampedModel):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    ai_match_score = models.FloatField(blank=True, null=True, help_text="AI-generated match score for the application")
    ai_match_summary = models.TextField(blank=True, null=True, help_text="AI-generated summary of the candidate's match for the job")
    cover_letter = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('candidate', 'job')