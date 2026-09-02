from rest_framework import serializers
from .models import CandidateDocument

class CandidateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateDocument
        fields = ['id', 'file', 'file_name', 'created_at']
        read_only_fields = ['file_name', 'created_at']