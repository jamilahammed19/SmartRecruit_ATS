from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job, AIInterviewQuestion
from .serializers import JobSerializer, AIInterviewQuestionSerializer
from .permissions import IsHRUserOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')  # Shows newest jobs first
    serializer_class = JobSerializer
    permission_classes = [IsHRUserOrReadOnly]

    # Optional: If you want candidates to only see "Open" jobs, you can filter the queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If the user is a candidate, hide completed/processing jobs
        if hasattr(self.request.user, 'candidateprofile'):
            return queryset.filter(status='open')
            
        # HR sees everything
        return queryset


class AIInterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = AIInterviewQuestion.objects.all()
    serializer_class = AIInterviewQuestionSerializer
    permission_classes = [IsAuthenticated, IsHRUserOrReadOnly]