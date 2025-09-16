from rest_framework.permissions import BasePermission

class IsAssignedUser(BasePermission):
    """
    Allow only the user who is assigned the task to update it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("Admin","SuperAdmin")
