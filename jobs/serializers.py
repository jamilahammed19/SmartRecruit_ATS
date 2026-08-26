from rest_framework import serializers
from .models import Job, AIInterviewQuestion




class BaseTimeStampedSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['created_at', 'updated_at']


class JobSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = Job


class AIInterviewQuestionSerializer(BaseTimeStampedSerializer):
    class Meta(BaseTimeStampedSerializer.Meta):
        model = AIInterviewQuestion