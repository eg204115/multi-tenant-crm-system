from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allow access only to Admin users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManagerOrAdmin(permissions.BasePermission):
    """Allow access to Manager and Admin users"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'manager']

class CanDelete(permissions.BasePermission):
    """Allow delete only for Admin users"""
    
    def has_permission(self, request, view):
        if view.action == 'destroy':
            return request.user.is_authenticated and request.user.role == 'admin'
        return True