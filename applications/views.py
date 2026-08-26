from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsHRUserOrCandidateOwner

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsHRUserOrCandidateOwner]

    def get_queryset(self):
        user = self.request.user
        
        # If HR, return all applications (newest first)
        if hasattr(user, 'hr_profile'):
            return Application.objects.all().order_by('-created_at')
            
        # If Candidate, only return applications they created
        if hasattr(user, 'candidate_profile'):
            return Application.objects.filter(candidate=user.candidate_profile).order_by('-created_at')
            
        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        
        # Ensure the user actually has a candidate profile before applying
        if not hasattr(user, 'candidate_profile'):
            raise ValidationError({"detail": "Only registered candidates can apply for jobs."})
        
        # Check if they already applied (acts as a backup to unique_together)
        job = serializer.validated_data.get('job')
        if Application.objects.filter(candidate=user.candidate_profile, job=job).exists():
            raise ValidationError({"detail": "You have already applied for this position."})

        # Automatically link the application to the logged-in candidate
        serializer.save(candidate=user.candidate_profile)