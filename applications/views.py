from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsHRUserOrCandidateOwner
from notifications.models import Notification

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
        
        if not hasattr(user, 'candidate_profile'):
            raise ValidationError({"detail": "Only registered candidates can apply for jobs."})
        
        job = serializer.validated_data.get('job')
        
        # --- NEW: Check if the deadline has passed ---
        if job.deadline and job.deadline < timezone.now().date():
            raise ValidationError({"detail": "This job application is closed. The deadline has passed."})
            
        if Application.objects.filter(candidate=user.candidate_profile, job=job).exists():
            raise ValidationError({"detail": "You have already applied for this position."})

        serializer.save(candidate=user.candidate_profile)

    def perform_update(self, serializer):
        user = self.request.user
        
        # 1. Get the old status before saving
        old_instance = self.get_object()
        old_status = old_instance.status
        
        # 2. Block candidates from changing their own status
        if hasattr(user, 'candidate_profile') and not hasattr(user, 'hr_profile'):
            if 'status' in serializer.validated_data:
                serializer.validated_data.pop('status')
                
        # 3. Save the update
        new_instance = serializer.save()

        # 4. If HR updated the status, generate the automatic notification
        if hasattr(user, 'hr_profile') and old_status != new_instance.status:
            status_messages = {
                'under_review': f"Great news! Your application for {new_instance.job.title} has been Shortlisted and is under review.",
                'rejected': f"Update on your application for {new_instance.job.title}: Unfortunately, we will not be moving forward at this time.",
                'offered': f"Congratulations! You have been Accepted for the {new_instance.job.title} position. We will contact you shortly.",
                'completed': f"The recruitment pipeline for {new_instance.job.title} has been closed."
            }
            
            if new_instance.status in status_messages:
                Notification.objects.create(
                    user=new_instance.candidate.user,
                    title="Application Status Updated",
                    message=status_messages[new_instance.status],
                    notification_type='application'
                )