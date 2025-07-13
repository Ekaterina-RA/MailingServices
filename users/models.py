from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    country = models.CharField(
        max_length=100, verbose_name="Страна", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Can block user"),
            ("can_view_client", "CCan viewc lient"),
            ("can_disable_mailing", "Can disable mailing"),
            ("can_view_mailing", "Can view mailing"),
            ("can_disable_message", "Can disable message"),
            ("can_view_message", "Can view message"),
            ("can_view_all", "Can view all items"),
            ("is_manager", "Has manager privileges"),
        ]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    country = models.CharField(
        max_length=100, verbose_name="Страна", null=True, blank=True
    )

    def __str__(self):
        return f"Профиль {self.user.username}"
