from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    # Added readable fields so your React frontend can display titles/names easily
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name', 
            'status', 'ai_match_score', 'ai_match_summary', 
            'cover_letter', 'created_at'
        ]
        # Prevent candidates from faking their status or AI scores
        read_only_fields = [
            'candidate', 'status', 'ai_match_score', 
            'ai_match_summary', 'created_at'
        ]