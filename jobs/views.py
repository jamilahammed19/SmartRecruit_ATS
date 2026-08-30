from rest_framework import viewsets
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Job, AIInterviewQuestion
from .serializers import JobSerializer, AIInterviewQuestionSerializer
from .permissions import IsHRUserOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        
        # --- THE MAGIC LAZY UPDATE ---
        # This single line safely updates the database for ANY job that 
        # is still 'open' but the deadline has passed.
        Job.objects.filter(status='open', deadline__lt=today).update(status='processing')

        # Now, return the querysets as normal
        if user.is_authenticated and hasattr(user, 'hr_profile'):
            # HR sees all jobs
            return Job.objects.all().order_by('-created_at')
            
        # Candidates only see jobs that are currently 'open' (and strictly >= today)
        return Job.objects.filter(deadline__gte=today, status='open').order_by('-created_at')


class AIInterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = AIInterviewQuestion.objects.all()
    serializer_class = AIInterviewQuestionSerializer
    permission_classes = [IsAuthenticated, IsHRUserOrReadOnly]