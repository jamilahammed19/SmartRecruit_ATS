from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, AIInterviewQuestionViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'interview_questions', AIInterviewQuestionViewSet, basename='interview-question')

urlpatterns = [
    # Include all the automatically generated ViewSet routes
    path('', include(router.urls)),
]