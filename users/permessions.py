from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    
# class IsLoggedin(BasePermission):

#     def has_permission(self, request, view):
#         return request.user