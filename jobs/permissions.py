from rest_framework import permissions

class IsHRUserOrReadOnly(permissions.BasePermission):
    """
    Allows anyone (including candidates) to view the list of jobs.
    Only allows users with an HRProfile to create, edit, or delete jobs.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS (Read-only operations)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For POST, PUT, PATCH, DELETE: check if they have an HR profile
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'hrprofile')
        )