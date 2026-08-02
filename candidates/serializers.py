from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    CandidateProfile, Address, Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, 
    PortfolioPublicationProject
)

User = get_user_model()

class BaseTimeStampedSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['created_at', 'updated_at']

# Personal Info is now part of CandidateProfile, so we create a serializer just for those fields
class PersonalInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        # Exclude relational and system fields so the user can only update their personal data
        exclude = ['id', 'user', 'created_at', 'updated_at']

class AddressSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Address
        exclude = ['created_at', 'updated_at', 'profile', 'address_type']

class EducationSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Education
        exclude = ['created_at', 'updated_at', 'profile']

class TrainingSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Training
        exclude = ['created_at', 'updated_at', 'profile']

class EmploymentSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Employment
        exclude = ['created_at', 'updated_at', 'profile']

class SkillSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Skill
        exclude = ['created_at', 'updated_at', 'profile']

class ExtracurricularActivitySerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = ExtracurricularActivity
        exclude = ['created_at', 'updated_at', 'profile']

class ReferenceSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Reference
        exclude = ['created_at', 'updated_at', 'profile']

class PortfolioPublicationProjectSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = PortfolioPublicationProject
        exclude = ['created_at', 'updated_at', 'profile']


class CandidateProfileReadSerializer(serializers.ModelSerializer):
    # We use MethodFields to structure the JSON exactly how React expects it
    personal_info = serializers.SerializerMethodField()
    present_address = serializers.SerializerMethodField()
    permanent_address = serializers.SerializerMethodField()
    
    educations = EducationSerializer(many=True, read_only=True)
    trainings = TrainingSerializer(many=True, read_only=True)
    employments = EmploymentSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    extracurricular_activities = ExtracurricularActivitySerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    portfolios_publications_projects = PortfolioPublicationProjectSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            'id', 'personal_info', 'present_address', 'permanent_address', 
            'educations', 'trainings', 'employments', 'skills', 
            'extracurricular_activities', 'references', 'portfolios_publications_projects'
        ]

    def get_personal_info(self, obj):
        # Passes the profile itself into the PersonalInfo serializer
        return PersonalInfoUpdateSerializer(obj).data

    def get_present_address(self, obj):
        # Filters the reverse relation for the present address
        address = obj.addresses.filter(address_type='present').first()
        return AddressSerializer(address).data if address else None

    def get_permanent_address(self, obj):
        # Filters the reverse relation for the permanent address
        address = obj.addresses.filter(address_type='permanent').first()
        return AddressSerializer(address).data if address else None