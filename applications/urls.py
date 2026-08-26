from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet

# Initialize the router
router = DefaultRouter()

# Register the application viewset
router.register(r'', ApplicationViewSet, basename='application')

urlpatterns = [
    # Include all generated routes (e.g., /api/applications/)
    path('', include(router.urls)),
]