import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        
        Job.objects.filter(status='open', deadline__lt=today).update(status='processing')

        if user.is_authenticated and hasattr(user, 'hr_profile'):
            return Job.objects.all().order_by('-created_at')
            
        return Job.objects.filter(deadline__gte=today, status='open').order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHRUserOrReadOnly])
    def generate_summary(self, request, pk=None):
        job = self.get_object()
        fastapi_url = "http://127.0.0.1:8001/api/ai/job-summary/"
        payload = {"title": job.title, "description": job.description, "requirements": job.requirements}
        headers = {"X-API-Key": "super-secret-smartrecruit-ats-key-2026"}

        try:
            response = requests.post(fastapi_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                job.ai_short_description = data.get('summary', '')
                job.save()
                return Response({'ai_short_description': job.ai_short_description})
            return Response({"error": "AI Engine failed to generate summary."}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHRUserOrReadOnly])
    def generate_questions(self, request, pk=None):
        job = self.get_object()
        fastapi_url = "http://127.0.0.1:8001/api/ai/job-questions/"
        payload = {"title": job.title, "description": job.description, "requirements": job.requirements}
        headers = {"X-API-Key": "super-secret-smartrecruit-ats-key-2026"}

        try:
            response = requests.post(fastapi_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                AIInterviewQuestion.objects.filter(job=job).delete()
                
                questions_data = data.get('questions', [])
                new_questions = []
                for q in questions_data:
                    obj = AIInterviewQuestion.objects.create(
                        job=job, 
                        question=q.get('question', ''), 
                        answer=q.get('answer', '')
                    )
                    new_questions.append({
                        "id": obj.id, "question": obj.question, "answer": obj.answer
                    })
                
                return Response(new_questions)
            return Response({"error": "AI Engine failed to generate questions."}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class AIInterviewQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = AIInterviewQuestionSerializer
    permission_classes = [IsAuthenticated, IsHRUserOrReadOnly]

    def get_queryset(self):
        job_id = self.request.query_params.get('job_id')
        if job_id:
            return AIInterviewQuestion.objects.filter(job_id=job_id)
        return AIInterviewQuestion.objects.all()