from rest_framework import permissions

class IsHROrReadOnly(permissions.BasePermission):
    """
    Allows Candidates to only view records. 
    Only HR can create, update, or delete Interviews.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'hr_profile')


class IsHROrCandidateRequestor(permissions.BasePermission):
    """
    Allows Candidates to create RescheduleRequests.
    Only HR can update or delete them (e.g. changing status to 'approved').
    """
    def has_permission(self, request, view):
        # Anyone authenticated can GET or POST
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        # Only HR can PUT, PATCH, DELETE
        return hasattr(request.user, 'hr_profile')