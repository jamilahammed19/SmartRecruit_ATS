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
        return CandidateDocument.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_documents_with_ai(request):
    user_docs = CandidateDocument.objects.filter(user=request.user).order_by('created_at')
    
    if not user_docs.exists():
        return Response({"error": "No documents found to process."}, status=400)

    FASTAPI_URL = "http://127.0.0.1:8001/api/ai/parse-cv/"
    
    multipart_form_data = []
    file_handles = []
    
    try:
        for doc in user_docs:
            content_type, _ = mimetypes.guess_type(doc.file.name)
            f = open(doc.file.path, 'rb')
            file_handles.append(f)
            
            multipart_form_data.append(
                ('files', (doc.file_name, f, content_type or 'application/octet-stream'))
            )
            
        headers = {
            "X-API-Key": "super-secret-smartrecruit-ats-key-2026"
        }
        
        response = requests.post(FASTAPI_URL, files=multipart_form_data, headers=headers)
        
        for f in file_handles:
            f.close()
            
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": f"AI Backend Error: {response.text}"}, status=response.status_code)
            
    except requests.exceptions.ConnectionError:
        for f in file_handles:
            if not f.closed:
                f.close()
        return Response({"error": "Cannot connect to AI Backend. Ensure FastAPI is running on port 8001."}, status=503)
    except Exception as e:
        for f in file_handles:
            if not f.closed:
                f.close()
        return Response({"error": str(e)}, status=500)