from rest_framework.permissions import BasePermission
from django.conf import settings


class HasInternalAPIKey(BasePermission):
    """
    Grants access only if request contains the correct internal API key.
    """
    def has_permission(self, request, view):
        key = request.headers.get("X-API-KEY")
        return key == settings.INTERNAL_API_KEY
