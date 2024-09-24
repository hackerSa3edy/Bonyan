from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "instructor"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "instructor"
