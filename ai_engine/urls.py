from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateDocumentViewSet, process_documents_with_ai

router = DefaultRouter()
router.register(r'documents', CandidateDocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('ai-process-documents/', process_documents_with_ai, name='ai-process'),
]