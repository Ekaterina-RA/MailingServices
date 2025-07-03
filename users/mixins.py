from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.role == "manager"


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "manager"


class UserAccessMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == "user":
            return queryset.filter(owner=self.request.user)
        return queryset
