from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, 
    PortfolioPublicationProject
)
from .serializers import (
    CandidateProfileReadSerializer, PersonalInfoSerializer, 
    AddressSerializer, EducationSerializer, TrainingSerializer, 
    EmploymentSerializer, SkillSerializer, ExtracurricularActivitySerializer,
    ReferenceSerializer, PortfolioPublicationProjectSerializer
)


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CandidateProfileReadSerializer


class CandidateProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateProfileReadSerializer

    def get_object(self):
        return self.request.user.candidateprofile


class BaseProfileSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(candidateprofile=self.request.user.candidateprofile)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.candidateprofile_set.add(self.request.user.candidateprofile)


class PersonalInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.candidateprofile.personal_info


class PresentAddressView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.candidateprofile.present_address


class PermanentAddressView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.candidateprofile.permanent_address


class EducationViewSet(BaseProfileSectionViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class TrainingViewSet(BaseProfileSectionViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer


class EmploymentViewSet(BaseProfileSectionViewSet):
    queryset = Employment.objects.all()
    serializer_class = EmploymentSerializer


class SkillViewSet(BaseProfileSectionViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ExtracurricularActivityViewSet(BaseProfileSectionViewSet):
    queryset = ExtracurricularActivity.objects.all()
    serializer_class = ExtracurricularActivitySerializer


class ReferenceViewSet(BaseProfileSectionViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class PortfolioPublicationProjectViewSet(BaseProfileSectionViewSet):
    queryset = PortfolioPublicationProject.objects.all()
    serializer_class = PortfolioPublicationProjectSerializer
