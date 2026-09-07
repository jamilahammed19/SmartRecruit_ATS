from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsCandidateUser
from .models import (
    CandidateProfile, Address, Education, Training, Employment, 
    Skill, ExtracurricularActivity, Reference, 
    PortfolioPublicationProject
)
from .serializers import (
    CandidateProfileReadSerializer, PersonalInfoUpdateSerializer, ProfilePictureSerializer, 
    AddressSerializer, EducationSerializer, TrainingSerializer, 
    EmploymentSerializer, SkillSerializer, ExtracurricularActivitySerializer,
    ReferenceSerializer, PortfolioPublicationProjectSerializer
)


class CandidateProfileView(generics.RetrieveAPIView):
    permission_classes = [IsCandidateUser]
    serializer_class = CandidateProfileReadSerializer

    def get_object(self):
        return self.request.user.candidate_profile


class PersonalInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalInfoUpdateSerializer
    permission_classes = [IsCandidateUser]

    def get_object(self):
        return self.request.user.candidate_profile


class ProfilePictureView(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsCandidateUser]
    parser_classes = [MultiPartParser, FormParser] 

    def get_object(self):
        return self.request.user.candidate_profile

class BaseAddressView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsCandidateUser]
    address_type = None

    def get_object(self):
        obj, created = Address.objects.get_or_create(
            profile=self.request.user.candidate_profile, 
            address_type=self.address_type
        )
        return obj

class PresentAddressView(BaseAddressView):
    address_type = 'present'

class PermanentAddressView(BaseAddressView):
    address_type = 'permanent'


class BaseProfileSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCandidateUser]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.candidate_profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.candidate_profile)


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