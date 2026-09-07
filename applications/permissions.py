from rest_framework import permissions

class IsHRUserOrCandidateOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'hr_profile'):
            return True
            
        if hasattr(request.user, 'candidate_profile'):
            return obj.candidate.user == request.user
            
        return False