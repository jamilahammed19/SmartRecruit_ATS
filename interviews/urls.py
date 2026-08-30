from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterviewViewSet, RescheduleRequestViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'schedules', InterviewViewSet, basename='interview')
router.register(r'reschedule-requests', RescheduleRequestViewSet, basename='reschedule-request')

urlpatterns = [
    path('', include(router.urls)),
]