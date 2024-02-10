from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print("         bogdaaaaaan    ")
        auth = JWTAuthentication()
        try:
            valid_data = auth.get_validated_token(request.headers.get('Authorization').split()[1])
            user_role = valid_data.get('role')
            return user_role == 'admin'
        except Exception as e:
            return False
