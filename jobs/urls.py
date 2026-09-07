from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, AIInterviewQuestionViewSet

# Initialize the router
router = DefaultRouter()

router.register(r'job_post', JobViewSet, basename='job')
router.register(r'interview_questions', AIInterviewQuestionViewSet, basename='interview-question')

urlpatterns = [
    path('', include(router.urls)),
]