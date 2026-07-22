from rest_framework import serializers
from django.contrib.auth.models import User
from candidates.models import CandidateProfile
from django.db import transaction

from rest_framework import serializers
from django.contrib.auth.models import User
from candidates.models import CandidateProfile, PersonalInfo, Address
from django.db import transaction

class CandidateRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if PersonalInfo.objects.filter(verified_email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        personal_info = PersonalInfo.objects.create()
        present_address = Address.objects.create()
        permanent_address = Address.objects.create()

        CandidateProfile.objects.create(
            user=user,
            personal_info=personal_info,
            present_address=present_address,
            permanent_address=permanent_address,
        )

        return user