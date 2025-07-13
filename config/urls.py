from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path(
        "admin/users/group/<path:object_id>/change/",
        RedirectView.as_view(pattern_name="admin:auth_group_change", permanent=True),
    ),
    path("admin/", admin.site.urls),
    path("", include("messaging.urls", namespace="messaging")),
    path("users/", include("users.urls", namespace="users")),
]
