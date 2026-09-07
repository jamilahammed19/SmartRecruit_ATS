from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from .models import Interview, RescheduleRequest
from .serializers import InterviewSerializer, RescheduleRequestSerializer
from .permissions import IsHROrReadOnly, IsHROrCandidateRequestor
from notifications.models import Notification


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsHROrReadOnly]

    def get_queryset(self):
        user = self.request.user
        
        if hasattr(user, 'hr_profile'):
            return Interview.objects.all().order_by('scheduled_time')
            
        if hasattr(user, 'candidate_profile'):
            return Interview.objects.filter(
                application__candidate=user.candidate_profile,
                scheduled_time__gte=timezone.now(),
                application__status='interview_scheduled'
            ).order_by('scheduled_time')
            
        return Interview.objects.none()

    def perform_create(self, serializer):
        interview = serializer.save()
        application = interview.application
        application.status = 'interview_scheduled'
        application.save()

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
        
        instance.delete()
        
        if application.status == 'interview_scheduled':
            application.status = 'under_review'
            application.save()
            
            Notification.objects.create(
                user=user,
                title="Interview Cancelled",
                message=f"Your previously scheduled interview for {job_title} has been cancelled by HR. Your application is back under review.",
                notification_type='interview'
            )

    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        interview = self.get_object()
        
        new_time = request.data.get('scheduled_time')
        new_link = request.data.get('meeting_link', interview.meeting_link)
        new_location = request.data.get('location', interview.location)

        if not new_time:
            return Response({"detail": "New scheduled time is required."}, status=status.HTTP_400_BAD_REQUEST)

        interview.scheduled_time = parse_datetime(new_time)
        interview.meeting_link = new_link
        interview.location = new_location
        interview.save()

        pending_requests = interview.reschedulerequest_set.filter(status='pending')
        if pending_requests.exists():
            pending_requests.update(status='approved')

        formatted_time = interview.scheduled_time.strftime("%b %d, %Y at %I:%M %p")
        Notification.objects.create(
            user=interview.application.candidate.user,
            title="Interview Rescheduled 📅",
            message=f"Your interview for {interview.application.job.title} has been successfully rescheduled to {formatted_time} by HR.",
            notification_type='interview'
        )

        return Response({"detail": "Interview successfully rescheduled."})

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
        interview = serializer.validated_data.get('interview')
        requested_time = serializer.validated_data.get('requested_time')
        
        now = timezone.now()

        # RULE 1: Cannot request a reschedule if the interview is starting in less than 2 hours
        if interview.scheduled_time < now + timedelta(hours=2):
            raise ValidationError({"detail": "Reschedule requests must be made at least 2 hours before the scheduled interview time."})
            
        # RULE 2: The NEW requested time must be at least 2 hours from now
        if requested_time < now + timedelta(hours=2):
            raise ValidationError({"detail": "The newly proposed time must be at least 2 hours from now."})

        # Security check: Ensure candidate owns the interview
        if hasattr(user, 'candidate_profile'):
            if interview.application.candidate != user.candidate_profile:
                raise PermissionDenied("You can only request to reschedule your own interviews.")
                
        serializer.save()