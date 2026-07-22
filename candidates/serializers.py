from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    PersonalInfo, Address, Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, 
    PortfolioPublicationProject, CandidateProfile
)

User = get_user_model()

class BaseTimeStampedSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['created_at', 'updated_at']

class PersonalInfoSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = PersonalInfo

class AddressSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Address

class EducationSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Education

class TrainingSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Training

class EmploymentSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Employment

class SkillSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Skill

class ExtracurricularActivitySerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = ExtracurricularActivity

class ReferenceSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Reference

class PortfolioPublicationProjectSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = PortfolioPublicationProject


class CandidateProfileReadSerializer(BaseTimeStampedSerializer):
    personal_info = PersonalInfoSerializer(read_only=True)
    present_address = AddressSerializer(read_only=True)
    permanent_address = AddressSerializer(read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    trainings = TrainingSerializer(many=True, read_only=True)
    employments = EmploymentSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    extracurricular_activities = ExtracurricularActivitySerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    portfolios_publications_projects = PortfolioPublicationProjectSerializer(many=True, read_only=True)

    class Meta(BaseTimeStampedSerializer.Meta):
        model = CandidateProfile
