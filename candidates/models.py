from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


GENDER_CHOICES = [
    ('male', 'Male'), 
    ('female', 'Female'), 
    ('other', 'Other')
]

RELIGION_CHOICES = [
    ('christianity', 'Christianity'), 
    ('islam', 'Islam'), 
    ('hinduism', 'Hinduism'), 
    ('buddhism', 'Buddhism'), 
    ('judaism', 'Judaism'), 
    ('other', 'Other')
]

MARITAL_STATUS_CHOICES = [
    ('single', 'Single'), 
    ('married', 'Married'), 
    ('divorced', 'Divorced'), 
    ('widowed', 'Widowed')
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

DEGREE_TYPE_CHOICES = [
    ('ssc', 'SSC'), 
    ('hsc', 'HSC'), 
    ('bachelors', 'Bachelors'), 
    ('masters', 'Masters'), 
    ('phd', 'PhD'),
    ('other', 'Other')    
]


class CandidateProfile(TimeStampedModel):
    """
    Master model for a candidate. Combines User link and Personal Info.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    
    # Personal Info
    photo = models.ImageField(upload_to='candidate/images/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    father_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    nid = models.CharField(max_length=20, unique=True, blank=True, null=True)
    passport_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    phone_number_alt = models.CharField(max_length=15, blank=True)
    verified_email = models.EmailField(unique=True, blank=True, null=True)
    email_alt = models.EmailField(blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.full_name or self.user.username}"


class Address(TimeStampedModel):
    ADDRESS_TYPES = (
        ('present', 'Present'),
        ('permanent', 'Permanent'),
    )
    
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    
    country = models.CharField(max_length=100, default='Bangladesh', blank=True)
    division = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    thana_upzila = models.CharField(max_length=100, blank=True)
    post_office = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    house_road_village = models.CharField(max_length=255, blank=True)

    class Meta:
        # Ensures a candidate doesn't have two "present" or two "permanent" addresses
        unique_together = ('profile', 'address_type')

    def __str__(self):
        return f"{self.get_address_type_display()} address for {self.profile}"


class Education(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='educations')
    
    degree_type = models.CharField(max_length=50, choices=DEGREE_TYPE_CHOICES, blank=True)
    degree_title = models.CharField(max_length=100, blank=True)
    board_university = models.CharField(max_length=255, blank=True)
    major_group = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    dept = models.CharField(max_length=255, blank=True)
    result = models.CharField(max_length=50, blank=True)
    scale = models.CharField(max_length=50, blank=True)
    passing_year = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.degree_title} - {self.profile}"


class Training(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='trainings')
    
    training_title = models.CharField(max_length=255, blank=True)
    institute = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.training_title} - {self.profile}"


class Employment(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='employments')
    
    organization_name = models.CharField(max_length=255, blank=True)
    organization_business = models.CharField(max_length=255, blank=True)
    organization_location = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    responsibilities = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.designation} at {self.organization_name} - {self.profile}"


class Skill(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skills')
    
    skill_name = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.skill_name} - {self.profile}"


class ExtracurricularActivity(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='extracurricular_activities')
    
    activity_name = models.CharField(max_length=255, blank=True)
    position_held = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.activity_name} - {self.profile}"


class Reference(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='references')
    
    name = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    phone_office = models.CharField(max_length=15, blank=True)
    relationship = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Ref: {self.name} for {self.profile}"


class PortfolioPublicationProject(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='portfolios_publications_projects')
    
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.profile}"