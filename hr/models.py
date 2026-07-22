# hr/models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

# Create your models here.


class HRProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_profile')
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/hr_profiles/', blank=True, null=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        display_name = full_name if full_name else self.user.username
        return f"{display_name} | {self.designation}"


