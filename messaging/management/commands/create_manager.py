from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from messaging.models import Mailing, Client, Message
from users.models import User


class Command(BaseCommand):
    help = "Настройка ролей и прав доступа для сервиса рассылок"

    def handle(self, *args, **options):
        # Создаем или обновляем группы
        user_group, _ = Group.objects.get_or_create(name="Пользователи")
        manager_group, _ = Group.objects.get_or_create(name="Менеджеры")

        # Настраиваем права
        self.setup_user_permissions(user_group)
        self.setup_manager_permissions(manager_group)

        self.stdout.write(self.style.SUCCESS("Права доступа успешно обновлены"))

    def setup_manager_permissions(self, group):
        """Расширенные права для менеджеров"""
        # Базовые права на модели
        models = [Client, Mailing, Message, User]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permissions)

        # Специальные права
        custom_perms = [
            ("users", "can_block_user"),
            ("users", "can_view_all"),
            ("users", "is_manager"),
            ("messaging", "can_disable_mailing"),
            ("messaging", "can_view_all_mailings"),
            ("messaging", "can_view_user_stats"),
        ]

        for app_label, codename in custom_perms:
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Permission {codename} not found in app {app_label}"
                    )
                )

    def setup_user_permissions(self, group):
        """Базовые права для обычных пользователей"""
        # Минимальные права на просмотр своих объектов
        self.add_model_permissions(
            group, Client, ["view", "add", "change"], own_only=True
        )
        self.add_model_permissions(group, Mailing, ["view", "add"], own_only=True)
        self.add_model_permissions(
            group, Message, ["view", "add", "change"], own_only=True
        )

    def add_model_permissions(self, group, model, actions, own_only=False):
        """Добавляет стандартные права на модель"""
        content_type = ContentType.objects.get_for_model(model)

        for action in actions:
            codename = f"{action}_{model._meta.model_name}"
            if own_only:
                codename = f"{action}_own_{model._meta.model_name}"

            try:
                perm = Permission.objects.get(
                    content_type=content_type, codename=codename
                )
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Permission {codename} not found for {model.__name__}"
                    )
                )

    def add_custom_permission(self, group, app_label, codename):
        """Добавляет кастомное право"""
        try:
            perm = Permission.objects.get(
                content_type__app_label=app_label, codename=codename
            )
            group.permissions.add(perm)
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    f"Permission {codename} not found in app {app_label}"
                )
            )
