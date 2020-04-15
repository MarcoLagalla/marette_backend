from rest_framework import permissions
from .models import Business, Customer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsPostOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'POST':
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return request.user and request.user.is_superuser


class OwnProfilePermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.user.id != obj.id:
            return False

        # obj here is a UserProfile instance
        return obj.user == request.user


class IsBusiness(permissions.BasePermission):
    def has_permission(self, request, view):

        try:
            business = Business.objects.get(user_id=request.user.id)
        except Business.DoesNotExist:
            return False

        return request.user or request.user.is_superuser


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):

        try:
            customer = Customer.objects.get(user_id=request.user.id)
        except Customer.DoesNotExist:
            return False

        return request.user or request.user.is_superuser