from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel
import datetime


GENDER_CHOICES = [
    ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
]

RELIGION_CHOICES = [
    ('islam', 'Islam'), ('hinduism', 'Hinduism'), ('christianity', 'Christianity'), 
    ('buddhism', 'Buddhism'), ('judaism', 'Judaism'), ('other', 'Other')
]

MARITAL_STATUS_CHOICES = [
    ('single', 'Single'), ('married', 'Married'), 
    ('divorced', 'Divorced'), ('widowed', 'Widowed')
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
]

DEGREE_TYPE_CHOICES = [
    ('ssc', 'SSC / Equivalent'), 
    ('hsc', 'HSC / Equivalent'), 
    ('diploma', 'Diploma'),
    ('bachelors', 'Bachelors'), 
    ('masters', 'Masters'), 
    ('phd', 'PhD'),
    ('other', 'Other')    
]

MAJOR_GROUP_TYPE_CHOICES = [
    ('science', 'Science'),
    ('arts', 'Arts / Humanities'),
    ('commerce', 'Commerce / Business Studies'),
    ('not_applicable', 'Not Applicable')
]

SCALE_CHOICES = [
    ('4.00', 'Out of 4.00'),
    ('5.00', 'Out of 5.00'),
    ('10.00', 'Out of 10.00'),
    ('100', 'Out of 100 (Percentage)'),
    ('other', 'Other')
]

EMPLOYMENT_TYPE_CHOICES = [
    ('full_time', 'Full-time'),
    ('part_time', 'Part-time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ('freelance', 'Freelance')
]

ITEM_TYPE_CHOICES = [
    ('project', 'Project'),
    ('publication', 'Publication / Research'),
    ('portfolio', 'Portfolio Website'),
    ('award', 'Award / Achievement'),
    ('other', 'Other')
]

DIVISION_CHOICES = [
    ('Barishal', 'Barishal'), ('Chittagong', 'Chittagong'), 
    ('Dhaka', 'Dhaka'), ('Khulna', 'Khulna'), 
    ('Mymensingh', 'Mymensingh'), ('Rajshahi', 'Rajshahi'), 
    ('Rangpur', 'Rangpur'), ('Sylhet', 'Sylhet')
]

DISTRICT_CHOICES = [
    ('Bagerhat', 'Bagerhat'), ('Bandarban', 'Bandarban'), ('Barguna', 'Barguna'), 
    ('Barishal', 'Barishal'), ('Bhola', 'Bhola'), ('Bogura', 'Bogura'), 
    ('Brahmanbaria', 'Brahmanbaria'), ('Chandpur', 'Chandpur'), ('Chapainawabganj', 'Chapainawabganj'), 
    ('Chittagong', 'Chittagong'), ('Chuadanga', 'Chuadanga'), ('Comilla', 'Comilla'), 
    ('Coxs Bazar', 'Coxs Bazar'), ('Dhaka', 'Dhaka'), ('Dinajpur', 'Dinajpur'), 
    ('Faridpur', 'Faridpur'), ('Feni', 'Feni'), ('Gaibandha', 'Gaibandha'), 
    ('Gazipur', 'Gazipur'), ('Gopalganj', 'Gopalganj'), ('Habiganj', 'Habiganj'), 
    ('Jamalpur', 'Jamalpur'), ('Jashore', 'Jashore'), ('Jhalokati', 'Jhalokati'), 
    ('Jhenaidah', 'Jhenaidah'), ('Joypurhat', 'Joypurhat'), ('Khagrachhari', 'Khagrachhari'), 
    ('Khulna', 'Khulna'), ('Kishoreganj', 'Kishoreganj'), ('Kurigram', 'Kurigram'), 
    ('Kushtia', 'Kushtia'), ('Lakshmipur', 'Lakshmipur'), ('Lalmonirhat', 'Lalmonirhat'), 
    ('Madaripur', 'Madaripur'), ('Magura', 'Magura'), ('Manikganj', 'Manikganj'), 
    ('Meherpur', 'Meherpur'), ('Moulvibazar', 'Moulvibazar'), ('Munshiganj', 'Munshiganj'), 
    ('Mymensingh', 'Mymensingh'), ('Naogaon', 'Naogaon'), ('Narail', 'Narail'), 
    ('Narayanganj', 'Narayanganj'), ('Narsingdi', 'Narsingdi'), ('Natore', 'Natore'), 
    ('Netrokona', 'Netrokona'), ('Nilphamari', 'Nilphamari'), ('Noakhali', 'Noakhali'), 
    ('Pabna', 'Pabna'), ('Panchagarh', 'Panchagarh'), ('Patuakhali', 'Patuakhali'), 
    ('Pirojpur', 'Pirojpur'), ('Rajbari', 'Rajbari'), ('Rajshahi', 'Rajshahi'), 
    ('Rangamati', 'Rangamati'), ('Rangpur', 'Rangpur'), ('Satkhira', 'Satkhira'), 
    ('Shariatpur', 'Shariatpur'), ('Sherpur', 'Sherpur'), ('Sirajganj', 'Sirajganj'), 
    ('Sunamganj', 'Sunamganj'), ('Sylhet', 'Sylhet'), ('Tangail', 'Tangail'), 
    ('Thakurgaon', 'Thakurgaon')
]

def current_year():
    return datetime.date.today().year


class CandidateProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    
    photo = models.ImageField(upload_to='candidate/images/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    father_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, default='Bangladeshi', blank=True)
    
    nid = models.CharField(max_length=30, unique=True, blank=True, null=True)
    passport_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number_alt = models.CharField(max_length=20, blank=True)
    verified_email = models.EmailField(unique=True, blank=True, null=True)
    email_alt = models.EmailField(blank=True)
    
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="Height in feet (e.g., 5.8)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")

    def __str__(self):
        return f"Profile of {self.full_name or self.user.username}"


class Address(TimeStampedModel):
    ADDRESS_TYPES = (('present', 'Present'), ('permanent', 'Permanent'))
    
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    
    country = models.CharField(max_length=100, default='Bangladesh', blank=True)
    division = models.CharField(max_length=100, choices=DIVISION_CHOICES, blank=True)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, blank=True)
    
    thana_upzila = models.CharField(max_length=100, blank=True)
    post_office = models.CharField(max_length=100, blank=True)
    post_code = models.PositiveIntegerField(blank=True, null=True) 
    house_road_village = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('profile', 'address_type')

    def __str__(self):
        return f"{self.get_address_type_display()} address for {self.profile}"


class Education(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='educations')
    
    degree_type = models.CharField(max_length=50, choices=DEGREE_TYPE_CHOICES, blank=True)
    degree_title = models.CharField(max_length=255, blank=True, help_text="e.g., BSc in Computer Science")
    board_university = models.CharField(max_length=255, blank=True)
    
    major_group_type = models.CharField(max_length=50, choices=MAJOR_GROUP_TYPE_CHOICES, blank=True)
    major_group = models.CharField(max_length=100, blank=True, help_text="e.g. Physics, Accounting")
    
    institution = models.CharField(max_length=255, blank=True)
    dept = models.CharField(max_length=255, blank=True)
    
    result = models.CharField(max_length=50, blank=True) 
    
    scale = models.CharField(max_length=50, choices=SCALE_CHOICES, blank=True)
    
    passing_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(current_year() + 5)],
        blank=True, null=True
    )
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., 4 Years")

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
    
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time', blank=True)
    
    organization_name = models.CharField(max_length=255, blank=True)
    organization_business = models.CharField(max_length=255, blank=True, help_text="e.g., Software IT, Bank")
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
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="e.g., 2.5")
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
    
    relationship = models.CharField(max_length=255, blank=True)
    
    mobile_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone_office = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Ref: {self.name} for {self.profile}"


class PortfolioPublicationProject(TimeStampedModel):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='portfolios_publications_projects')
    
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES, default='project', blank=True)
    
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title} - {self.profile}"