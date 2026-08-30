from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone  # <-- NEW: Needed to filter past dates
from .models import Interview, RescheduleRequest
from .serializers import InterviewSerializer, RescheduleRequestSerializer
from .permissions import IsHROrReadOnly, IsHROrCandidateRequestor
from notifications.models import Notification  # <-- NEW: To send automatic alerts


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsHROrReadOnly]

    def get_queryset(self):
        user = self.request.user
        
        # HR sees ALL interviews (past, present, and cancelled)
        if hasattr(user, 'hr_profile'):
            return Interview.objects.all().order_by('scheduled_time')
            
        # Candidates ONLY see interviews that are in the future AND currently active
        if hasattr(user, 'candidate_profile'):
            return Interview.objects.filter(
                application__candidate=user.candidate_profile,
                scheduled_time__gte=timezone.now(),           # Must be in the future
                application__status='interview_scheduled'     # Must not be rejected/reverted
            ).order_by('scheduled_time')
            
        return Interview.objects.none()

    def perform_create(self, serializer):
        interview = serializer.save()
        
        # Automatically update the application status
        application = interview.application
        application.status = 'interview_scheduled'
        application.save()

        # --- NEW: Send Notification to Candidate ---
        formatted_time = interview.scheduled_time.strftime("%b %d, %Y at %I:%M %p")
        Notification.objects.create(
            user=application.candidate.user,
            title="Interview Scheduled! 📅",
            message=f"An interview for {application.job.title} has been scheduled on {formatted_time}. Please check your interview panel for details.",
            notification_type='interview'
        )

    def perform_destroy(self, instance):
        application = instance.application
        user = application.candidate.user
        job_title = application.job.title
        
        instance.delete() # Delete the interview
        
        # If the application was 'interview_scheduled', revert it back to 'under_review'
        # so HR can schedule them again later if needed.
        if application.status == 'interview_scheduled':
            application.status = 'under_review'
            application.save()
            
            # --- NEW: Send Cancellation Notification to Candidate ---
            Notification.objects.create(
                user=user,
                title="Interview Cancelled",
                message=f"Your previously scheduled interview for {job_title} has been cancelled by HR. Your application is back under review.",
                notification_type='interview'
            )


class RescheduleRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RescheduleRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsHROrCandidateRequestor]

    def get_queryset(self):
        user = self.request.user
        
        if hasattr(user, 'hr_profile'):
            return RescheduleRequest.objects.all().order_by('-created_at')
            
        if hasattr(user, 'candidate_profile'):
            return RescheduleRequest.objects.filter(
                interview__application__candidate=user.candidate_profile
            ).order_by('-created_at')
            
        return RescheduleRequest.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        
        # If a candidate is making the request, ensure they actually own the interview
        if hasattr(user, 'candidate_profile'):
            interview = serializer.validated_data.get('interview')
            if interview.application.candidate != user.candidate_profile:
                raise PermissionDenied("You can only request to reschedule your own interviews.")
                
        serializer.save()