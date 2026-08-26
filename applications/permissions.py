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
            
        # Candidates can only view or interact with their own application
        if hasattr(request.user, 'candidateprofile'):
            return obj.candidate.user == request.user
            
        return False