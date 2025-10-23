from rest_framework import permissions

class IsWpfOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        secret_key = request.headers.get('X-WPF-KEY')
        if secret_key == "tahina_secret_123":
            return True
        return request.user and request.user.is_authenticated
