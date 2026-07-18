from django.db import models
from core.models import TimeStampedModel

# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'), 
    ('F', 'Female'), 
    ('O', 'Other')
]

RELIGION_CHOICES = [
    ('C', 'Christianity'), 
    ('I', 'Islam'), 
    ('H', 'Hinduism'), 
    ('B', 'Buddhism'), 
    ('J', 'Judaism'), 
    ('O', 'Other')
]

MARITAL_STATUS_CHOICES = [
    ('S', 'Single'), 
    ('M', 'Married'), 
    ('D', 'Divorced'), 
    ('W', 'Widowed')
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
    ('SSC', 'SSC'), 
    ('HSC', 'HSC'), 
    ('Bachelors', 'Bachelors'), 
    ('Masters', 'Masters'), 
    ('PhD', 'PhD'),
    ('Other', 'Other')    
]


class PersonalInfo(TimeStampedModel):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=1, choices=RELIGION_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=100)
    nid = models.CharField(max_length=20, unique=True)
    passport_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    phone_number_alt = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_alt = models.EmailField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
  
    class Meta:
        abstract = True
    

class Address(TimeStampedModel):
    country = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    house_road_village = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Education(TimeStampedModel):
    degree_type = models.CharField(max_length=50, choices=DEGREE_TYPE_CHOICES)
    degree_title = models.CharField(max_length=100)
    board_university = models.CharField(max_length=255)
    major_group = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=255)
    dept = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=50)
    scale = models.CharField(max_length=50)
    passing_year = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Training(TimeStampedModel):
    training_title = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True


class Employment(TimeStampedModel):
    organization_name = models.CharField(max_length=255)
    organization_business = models.CharField(max_length=255, blank=True, null=True)
    organization_location = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Skill(TimeStampedModel):
    skill_name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class ExtracurricularActivity(TimeStampedModel):
    activity_name = models.CharField(max_length=255)
    position_held = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Reference(TimeStampedModel):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_office = models.CharField(max_length=15, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class PortfolioPublicationProject(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True


class CandidateProfile(TimeStampedModel):
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