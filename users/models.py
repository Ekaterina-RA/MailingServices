from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Mailing, MailingAttempt


class User(AbstractUser):
    ROLES = (
        ("user", "Пользователь"),
        ("manager", "Менеджер"),
    )

    role = models.CharField(max_length=10, choices=ROLES, default="user")
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "users_user"
        swappable = "AUTH_USER_MODEL"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Группы",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь",
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="Права доступа",
        blank=True,
        help_text="Особенные права для этого пользователя",
        related_name="custom_user_set",
        related_query_name="user",
    )

    def clean(self):
        super().clean()
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError({"email": "Введите корректный email адрес"})

    def is_manager(self):
        return self.role == "manager" or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class UserStats(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="stats",
        verbose_name="Пользователь",
    )
    total_mailings = models.PositiveIntegerField(
        default=0, verbose_name="Всего рассылок"
    )
    active_mailings = models.PositiveIntegerField(
        default=0, verbose_name="Активных рассылок"
    )
    successful_attempts = models.PositiveIntegerField(
        default=0, verbose_name="Успешных попыток"
    )
    failed_attempts = models.PositiveIntegerField(
        default=0, verbose_name="Неудачных попыток"
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )

    class Meta:
        verbose_name = "Статистика пользователя"
        verbose_name_plural = "Статистика пользователей"

    def update_stats(self):
        mailings = Mailing.objects.filter(owner=self.user)
        attempts = MailingAttempt.objects.filter(mailing__in=mailings)

        self.total_mailings = mailings.count()
        self.active_mailings = mailings.filter(status="started").count()
        self.successful_attempts = attempts.filter(status="success").count()
        self.failed_attempts = attempts.filter(status="failed").count()
        self.save()

    def __str__(self):
        return f"Статистика {self.user.username}"


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)
