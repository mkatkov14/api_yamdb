from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsModer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moder

#class IsAuthorOrReadOnly(permissions.BasePermission):
#
#   def has_object_permission(self, request, view, obj):
#        return (request.method in permissions.SAFE_METHODS
#                or obj.author == request.user)
