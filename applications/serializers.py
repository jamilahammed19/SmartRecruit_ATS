from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    
    # User Model Fields
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    
    # Profile Fields
    candidate_education = serializers.CharField(source='candidate.education', read_only=True, default='')
    candidate_experience = serializers.IntegerField(source='candidate.experience_years', read_only=True, default=0)
    candidate_skills = serializers.CharField(source='candidate.skills', read_only=True, default='')
    
    # --- NEW: Full Profile Additional Fields ---
    candidate_bio = serializers.CharField(source='candidate.bio', read_only=True, default='')
    candidate_portfolio = serializers.URLField(source='candidate.portfolio', read_only=True, default='')
    candidate_resume = serializers.FileField(source='candidate.resume', read_only=True, default=None)

    candidate_user_id = serializers.IntegerField(source='candidate.user.id', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name', 'candidate_email', 'candidate_user_id',
            'candidate_education', 'candidate_experience', 'candidate_skills',
            'candidate_bio', 'candidate_portfolio', 'candidate_resume',
            'status', 'ai_match_score', 'ai_match_summary', 
            'cover_letter', 'created_at'
        ]
        # Keep status out of read_only_fields so HR can update it
        read_only_fields = ['candidate', 'ai_match_score', 'ai_match_summary', 'created_at']