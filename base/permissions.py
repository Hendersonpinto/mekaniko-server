from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # The super() will check if the class at which we are inheriting from (IsAdminUser) has a has_permission method and what value it returns (true for admins, false for not admins)
        # This line triggers has_permission on the permissions.IsAdminUser class
        is_admin = super().has_permission(request, view)

        # If the method is within SAFE_METHODS: ['GET', 'HEAD', 'OPTIONS'] or if the user is an admin, we return true
        return request.method in permissions.SAFE_METHODS or is_admin
