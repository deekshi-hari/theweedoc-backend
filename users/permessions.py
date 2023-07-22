from rest_framework.permissions import BasePermission
from .models import User


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.user_type == "superadmin"
    

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.user_type == "admin"