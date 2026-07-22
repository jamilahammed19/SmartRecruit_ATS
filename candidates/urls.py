from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PersonalInfoView,
    PresentAddressView,
    PermanentAddressView,
    CandidateProfileView,
    EducationViewSet,
    TrainingViewSet,
    EmploymentViewSet,
    SkillViewSet,
    ExtracurricularActivityViewSet,
    ReferenceViewSet,
    PortfolioPublicationProjectViewSet
)

router = DefaultRouter()

router.register(r'education', EducationViewSet, basename='education')
router.register(r'trainings', TrainingViewSet, basename='training')
router.register(r'employments', EmploymentViewSet, basename='employment')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'extracurriculars', ExtracurricularActivityViewSet, basename='extracurricular')
router.register(r'references', ReferenceViewSet, basename='reference')
router.register(r'portfolios', PortfolioPublicationProjectViewSet, basename='portfolio')

urlpatterns = [
    path('profile/', CandidateProfileView.as_view(), name='candidate-profile'),
    path('personal_info/', PersonalInfoView.as_view(), name='personal-info'),
    path('present_address/', PresentAddressView.as_view(), name='present-address'),
    path('permanent_address/', PermanentAddressView.as_view(), name='permanent-address'),
    path('', include(router.urls)),
]