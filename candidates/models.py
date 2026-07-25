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


class PersonalInfo(TimeStampedModel):
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
    

class Address(TimeStampedModel):
    country = models.CharField(max_length=100, default='Bangladesh', blank=True)
    division = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    thana_upzila = models.CharField(max_length=100, blank=True)
    post_office = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    house_road_village = models.CharField(max_length=255, blank=True)


class Education(TimeStampedModel):
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


class Training(TimeStampedModel):
    training_title = models.CharField(max_length=255, blank=True)
    institute = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Employment(TimeStampedModel):
    organization_name = models.CharField(max_length=255, blank=True)
    organization_business = models.CharField(max_length=255, blank=True)
    organization_location = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    responsibilities = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)


class Skill(TimeStampedModel):
    skill_name = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)


class ExtracurricularActivity(TimeStampedModel):
    activity_name = models.CharField(max_length=255, blank=True)
    position_held = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class Reference(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    phone_office = models.CharField(max_length=15, blank=True)
    relationship = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)


class PortfolioPublicationProject(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)


class CandidateProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE)
    present_address = models.OneToOneField(Address, related_name='present_address', on_delete=models.CASCADE)
    permanent_address = models.OneToOneField(Address, related_name='permanent_address', on_delete=models.CASCADE)
    educations = models.ManyToManyField(Education, blank=True)
    trainings = models.ManyToManyField(Training, blank=True)
    employments = models.ManyToManyField(Employment, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    extracurricular_activities = models.ManyToManyField(ExtracurricularActivity, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    portfolios_publications_projects = models.ManyToManyField(PortfolioPublicationProject, blank=True)

    def __str__(self):
        return f"Profile of {self.personal_info.full_name}"