from django.db import models

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


class PersonalInfo(models.Model):
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

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
    
    class Meta:
        abstract = True
    

class Address(models.Model):
    country = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    house_road_village = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Education(models.Model):
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

