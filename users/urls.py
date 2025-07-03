from django.urls import path

from .apps import UsersConfig
from .views import (
    CustomLoginView,
    RegisterView,
    custom_logout,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    activate_email,
    StatsView,
    BlockUserView,
    DisableMailingView,
)

app_name = UsersConfig.name


urlpatterns = [
    # Аутентификация
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", custom_logout, name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("activate/<uidb64>/<token>/", activate_email, name="activate_email"),
    # Статистика
    path("stats/", StatsView.as_view(), name="user_stats"),
    # Действия менеджера
    path("block_user/<int:pk>/", BlockUserView.as_view(), name="block_user"),
    path(
        "disable_mailing/<int:pk>/",
        DisableMailingView.as_view(),
        name="disable_mailing",
    ),
]
