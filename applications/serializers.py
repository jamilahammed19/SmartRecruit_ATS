from rest_framework import serializers
from .models import Application
from candidates.models import (
    CandidateProfile, Address, Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, PortfolioPublicationProject
)

# --- 1. Create Quick Nested Serializers for the Full Profile ---
class AddressSerializer(serializers.ModelSerializer):
    class Meta: model = Address; fields = '__all__'
class EducationSerializer(serializers.ModelSerializer):
    class Meta: model = Education; fields = '__all__'
class EmploymentSerializer(serializers.ModelSerializer):
    class Meta: model = Employment; fields = '__all__'
class SkillSerializer(serializers.ModelSerializer):
    class Meta: model = Skill; fields = '__all__'
class TrainingSerializer(serializers.ModelSerializer):
    class Meta: model = Training; fields = '__all__'
class ExtracurricularSerializer(serializers.ModelSerializer):
    class Meta: model = ExtracurricularActivity; fields = '__all__'
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta: model = Reference; fields = '__all__'
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta: model = PortfolioPublicationProject; fields = '__all__'

class FullCandidateProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    employments = EmploymentSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    trainings = TrainingSerializer(many=True, read_only=True)
    extracurricular_activities = ExtracurricularSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    portfolios_publications_projects = PortfolioSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateProfile
        fields = '__all__'

# --- 2. Attach it to your existing ApplicationSerializer ---
class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    
    # Simple summary fields for the list view
    candidate_education = serializers.CharField(source='candidate.education', read_only=True, default='')
    candidate_experience = serializers.IntegerField(source='candidate.experience_years', read_only=True, default=0)
    candidate_skills = serializers.CharField(source='candidate.skills', read_only=True, default='')

    # THE MAGIC LINE: This embeds the ENTIRE profile into the application response!
    full_profile = FullCandidateProfileSerializer(source='candidate', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name', 'candidate_email', 
            'candidate_education', 'candidate_experience', 'candidate_skills',
            'status', 'ai_match_score', 'ai_match_summary', 
            'cover_letter', 'created_at', 'full_profile'  # <-- Added full_profile here
        ]
        read_only_fields = ['candidate', 'ai_match_score', 'ai_match_summary', 'created_at', 'full_profile']