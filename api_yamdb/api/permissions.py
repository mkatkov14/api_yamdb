from rest_framework import permissions


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
