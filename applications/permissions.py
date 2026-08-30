from rest_framework import permissions

class IsHRUserOrCandidateOwner(permissions.BasePermission):
    """
    Candidates can view and create their own applications.
    HR can view and modify all applications.
    """
    def has_object_permission(self, request, view, obj):
        # HR can do anything with the application (edit status, add AI score, etc)
        if hasattr(request.user, 'hr_profile'):
            return True
            
        # FIXED: Added the underscore to match your views.py exactly
        if hasattr(request.user, 'candidate_profile'):
            return obj.candidate.user == request.user
            
        return False