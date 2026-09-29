from rest_framework import permissions


class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


class IsOfferingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organization.owner_id == request.user.id