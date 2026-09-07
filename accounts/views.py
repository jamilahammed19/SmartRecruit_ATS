from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import CandidateRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CandidateRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CandidateRegistrationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    user = request.user
    
    if hasattr(user, 'hr_profile'):
        return Response({'role': 'hr', 'name': user.first_name or user.username})
    elif hasattr(user, 'candidate_profile'):
        return Response({'role': 'candidate', 'name': user.first_name or user.username})
    elif user.is_superuser:
        return Response({'role': 'admin', 'name': 'Administrator'})
    
    return Response({'role': 'unknown'}, status=400)