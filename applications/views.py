from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsHRUserOrCandidateOwner
from notifications.models import Notification
import requests
from rest_framework.decorators import action
from rest_framework.response import Response

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsHRUserOrCandidateOwner]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'hr_profile'):
            return Application.objects.all().order_by('-created_at')
        if hasattr(user, 'candidate_profile'):
            return Application.objects.filter(candidate=user.candidate_profile).order_by('-created_at')
        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        
        if not hasattr(user, 'candidate_profile'):
            raise ValidationError({"detail": "Only registered candidates can apply for jobs."})
        
        candidate = user.candidate_profile

        missing_requirements = []

        if not candidate.photo:
            missing_requirements.append("Profile Picture")

        required_personal_fields = [
            candidate.full_name, candidate.father_name, candidate.mother_name,
            candidate.date_of_birth, candidate.gender, candidate.religion,
            candidate.marital_status, candidate.nationality, candidate.nid,
            candidate.phone_number, candidate.blood_group
        ]
        if not all(required_personal_fields):
            missing_requirements.append("All Personal Information Fields")

        def is_address_complete(addr):
            if not addr: return False
            return all([
                addr.country, addr.division, addr.district, 
                addr.thana_upzila, addr.post_office, addr.post_code, 
                addr.house_road_village
            ])

        present_address = candidate.addresses.filter(address_type='present').first()
        permanent_address = candidate.addresses.filter(address_type='permanent').first()

        if not is_address_complete(present_address):
            missing_requirements.append("Complete Present Address")
            
        if not is_address_complete(permanent_address):
            missing_requirements.append("Complete Permanent Address")

        has_ssc = candidate.educations.filter(degree_type__iexact='ssc').exists()
        has_hsc = candidate.educations.filter(degree_type__iexact='hsc').exists()
        if not has_ssc or not has_hsc:
            missing_requirements.append("Minimum SSC and HSC Education")

        if candidate.references.count() < 2:
            missing_requirements.append("At least Two References")

        if missing_requirements:
            raise ValidationError({
                "detail": "Profile incomplete. Please fill up all basic information first.",
                "missing": missing_requirements
            })


        job = serializer.validated_data.get('job')
        
        if job.deadline and job.deadline < timezone.now().date():
            raise ValidationError({"detail": "This job application is closed. The deadline has passed."})
            
        if Application.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError({"detail": "You have already applied for this position."})

        application = serializer.save(candidate=candidate)

        try:
            skills_list = [skill.skill_name for skill in candidate.skills.all() if skill.skill_name]
            candidate_skills = ", ".join(skills_list) if skills_list else "None listed"

            edu_list = [f"{edu.degree_title} from {edu.institution}" for edu in candidate.educations.all() if edu.degree_title]
            candidate_education = ", ".join(edu_list) if edu_list else "None listed"

            total_exp_years = 0
            for emp in candidate.employments.all():
                if emp.start_date:
                    end_year = emp.end_date.year if emp.end_date else timezone.now().year
                    total_exp_years += max(1, end_year - emp.start_date.year)

            payload = {
                "job_title": job.title,
                "job_description": getattr(job, 'description', 'No description provided.'),
                "candidate_skills": candidate_skills,
                "candidate_education": candidate_education,
                "candidate_experience": total_exp_years,
                "candidate_bio": candidate.full_name or "Applicant"
            }

            FASTAPI_URL = "http://127.0.0.1:8001/api/ai/score-application/"
            headers = {"X-API-Key": "super-secret-smartrecruit-ats-key-2026", "Content-Type": "application/json"}

            response = requests.post(FASTAPI_URL, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                application.ai_match_score = data.get('ai_match_score')
                application.ai_match_summary = data.get('ai_match_summary')
                application.save()
                
        except Exception as e:
            print(f"Auto AI Scoring failed during application submission: {e}")
            pass


    def perform_update(self, serializer):
        user = self.request.user
        old_instance = self.get_object()
        old_status = old_instance.status
        
        if hasattr(user, 'candidate_profile') and not hasattr(user, 'hr_profile'):
            if 'status' in serializer.validated_data:
                serializer.validated_data.pop('status')
                
        new_instance = serializer.save()

        if hasattr(user, 'hr_profile') and old_status != new_instance.status:
            status_messages = {
                'under_review': f"Great news! Your application for {new_instance.job.title} has been Shortlisted and is under review.",
                'rejected': f"Update on your application for {new_instance.job.title}: Unfortunately, we will not be moving forward at this time.",
                'offered': f"Congratulations! You have been Accepted for the {new_instance.job.title} position. We will contact you shortly.",
                'completed': f"The recruitment pipeline for {new_instance.job.title} has been closed."
            }
            if new_instance.status in status_messages:
                Notification.objects.create(
                    user=new_instance.candidate.user, title="Application Status Updated",
                    message=status_messages[new_instance.status], notification_type='application'
                )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def run_ai_scoring(self, request, pk=None):
        if not hasattr(request.user, 'hr_profile'):
            return Response({"error": "Only HR can run AI scoring."}, status=403)

        application = self.get_object()
        candidate = application.candidate
        
        if application.ai_match_score is not None:
            return Response({"error": "Already scored"}, status=400)

        skills_list = [skill.skill_name for skill in candidate.skills.all() if skill.skill_name]
        candidate_skills = ", ".join(skills_list) if skills_list else "None listed"

        edu_list = [f"{edu.degree_title} from {edu.institution}" for edu in candidate.educations.all() if edu.degree_title]
        candidate_education = ", ".join(edu_list) if edu_list else "None listed"

        total_exp_years = 0
        for emp in candidate.employments.all():
            if emp.start_date:
                end_year = emp.end_date.year if emp.end_date else timezone.now().year
                total_exp_years += max(1, end_year - emp.start_date.year)

        payload = {
            "job_title": application.job.title,
            "job_description": getattr(application.job, 'description', 'No description provided.'),
            "candidate_skills": candidate_skills,
            "candidate_education": candidate_education,
            "candidate_experience": total_exp_years,
            "candidate_bio": candidate.full_name or "Applicant"
        }

        FASTAPI_URL = "http://127.0.0.1:8001/api/ai/score-application/"
        headers = {"X-API-Key": "super-secret-smartrecruit-ats-key-2026", "Content-Type": "application/json"}

        try:
            response = requests.post(FASTAPI_URL, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                application.ai_match_score = data.get('ai_match_score')
                application.ai_match_summary = data.get('ai_match_summary')
                application.save()
                return Response({"message": "Scored successfully", "ai_match_score": application.ai_match_score, "ai_match_summary": application.ai_match_summary})
            else:
                return Response({"error": f"AI Engine Failed: {response.text}"}, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response({"error": "Cannot connect to AI Server (Port 8001)."}, status=503)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
