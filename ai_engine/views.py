from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CandidateDocument
from .serializers import CandidateDocumentSerializer
import requests
import mimetypes

class CandidateDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Candidates can only view and manage their own documents
        return CandidateDocument.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_documents_with_ai(request):
    """
    Grabs the candidate's latest document, sends it to the FastAPI microservice,
    and returns the structured JSON back to React.
    """
    latest_doc = CandidateDocument.objects.filter(user=request.user).order_by('-created_at').first()
    
    if not latest_doc:
        return Response({"error": "No documents found to process."}, status=400)

    # URL of your FastAPI Microservice
    FASTAPI_URL = "http://127.0.0.1:8001/api/ai/parse-cv/"
    
    try:
        # Dynamically determine content type so FastAPI accepts it
        content_type, _ = mimetypes.guess_type(latest_doc.file.name)
        
        with open(latest_doc.file.path, 'rb') as f:
            files = {'file': (latest_doc.file_name, f, content_type or 'application/octet-stream')}
            
            # --- NEW: ADD HEADERS HERE ---
            headers = {
                "X-API-Key": "super-secret-smartrecruit-ats-key-2026"
            }
            
            # Send HTTP POST to FastAPI WITH THE KEY
            response = requests.post(FASTAPI_URL, files=files, headers=headers)
            
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": f"AI Backend Error: {response.text}"}, status=response.status_code)
            
    except requests.exceptions.ConnectionError:
        return Response({"error": "Cannot connect to AI Backend. Ensure FastAPI is running on port 8001."}, status=503)
    except Exception as e:
        return Response({"error": str(e)}, status=500)