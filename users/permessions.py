from rest_framework.permissions import BasePermission
from .models import User


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == "superadmin":
            return request.user
    

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        print(request.user.user_type)
        if request.user.user_type == "admin" or request.user.user_type == "superadmin":
            return request.user