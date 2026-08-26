# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CandidateRegistrationView, get_user_role

urlpatterns = [
    path('register/candidate/', CandidateRegistrationView.as_view(), name='register-candidate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', get_user_role, name='auth-me')
]