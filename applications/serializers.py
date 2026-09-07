from rest_framework import serializers
from datetime import date
from .models import Application
from candidates.models import (
    CandidateProfile, Address, Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, PortfolioPublicationProject
)

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

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    
    candidate_education = serializers.SerializerMethodField()
    candidate_experience = serializers.SerializerMethodField()
    candidate_skills = serializers.SerializerMethodField()

    full_profile = FullCandidateProfileSerializer(source='candidate', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name', 'candidate_email', 
            'candidate_education', 'candidate_experience', 'candidate_skills',
            'status', 'ai_match_score', 'ai_match_summary', 
            'cover_letter', 'created_at', 'full_profile'
        ]
        read_only_fields = ['candidate', 'ai_match_score', 'ai_match_summary', 'created_at', 'full_profile']

    def get_candidate_education(self, obj):
        educations = obj.candidate.educations.all()
        if not educations:
            return ""
        return ", ".join([f"{e.degree_type} {e.degree_title}".strip() for e in educations])

    def get_candidate_experience(self, obj):
        total_days = 0
        for emp in obj.candidate.employments.all():
            if emp.start_date:
                end = emp.end_date if emp.end_date and not emp.is_current else date.today()
                total_days += (end - emp.start_date).days
        
        return round(total_days / 365.25, 1)

    def get_candidate_skills(self, obj):
        skills = obj.candidate.skills.all()
        if not skills:
            return ""
        return ", ".join([s.skill_name for s in skills])