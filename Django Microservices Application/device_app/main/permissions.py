from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print("debug1")
        auth = TokenAuthentication()
        print("debug2")
        try:
            user_auth_tuple = auth.authenticate(request)
            print("debug3")
            if user_auth_tuple is not None:
                user, token = user_auth_tuple
                print("debug4" + user.is_staff)
                return user.is_staff
        except AuthenticationFailed:
            print("error")
        return False