from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class CandidateDocument(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='candidate/documents/')
    file_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Document for {self.user.username}"