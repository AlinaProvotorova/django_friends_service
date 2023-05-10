from rest_framework.permissions import BasePermission


class RegistrationPermission(BasePermission):
    def has_permission(self, request, view):
        if view.basename == 'user-registration':
            return True

        return request.user and request.user.is_authenticated
