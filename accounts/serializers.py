from rest_framework import serializers
from django.contrib.auth.models import User
from candidates.models import CandidateProfile, Address
from django.db import transaction

class CandidateRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        # Ensure email is unique in the base User model
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
            
        # Ensure email is unique in the CandidateProfile model
        if CandidateProfile.objects.filter(verified_email=value).exists():
            raise serializers.ValidationError("A profile with this email already exists.")
            
        return value

    @transaction.atomic
    def create(self, validated_data):
        # 1. Create the base User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        # 2. Create the CandidateProfile
        # PersonalInfo fields are now built-in, so we can save the email directly here
        profile = CandidateProfile.objects.create(
            user=user,
            verified_email=validated_data['email']
        )

        # 3. Initialize empty addresses using the new ForeignKey relation
        Address.objects.create(profile=profile, address_type='present')
        Address.objects.create(profile=profile, address_type='permanent')

        return user