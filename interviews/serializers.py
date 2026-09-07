from rest_framework import serializers
from .models import Interview, RescheduleRequest

class RescheduleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RescheduleRequest
        fields = ['id', 'interview', 'requested_time', 'reason', 'status', 'created_at']
        read_only_fields = ['status', 'created_at'] 


class InterviewSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    candidate_name = serializers.CharField(source='application.candidate.user.username', read_only=True)

    application_status = serializers.CharField(source='application.status', read_only=True)
    
    reschedule_requests = RescheduleRequestSerializer(source='reschedulerequest_set', many=True, read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'job_title', 'candidate_name', 'application_status', 
            'scheduled_time', 'duration', 'location', 
            'meeting_link', 'notes', 'reschedule_requests', 'created_at'
        ]