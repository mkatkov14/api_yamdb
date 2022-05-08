from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_admin)


class IsModer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moder

# Сделал сначала суперов и админов отдельно,
# не сработало, позже буду разбираться.
# Полезно будет разделить, если захотим забрать
# у админов права и оставить только у суперов.
class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminModerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
    )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                obj.author == request.user
                or (request.user.is_authenticated and request.user.is_moder)
                or (request.user.is_authenticated and request.user.is_admin)
            )
        )
