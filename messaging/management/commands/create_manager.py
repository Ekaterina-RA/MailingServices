from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from messaging.models import Mailing, Client, Message


class Command(BaseCommand):
    help = 'Настройка ролей и прав доступа для сервиса рассылок'

    def handle(self, *args, **options):
        # Создаем или обновляем группы
        user_group, _ = Group.objects.get_or_create(name='Пользователи')
        manager_group, _ = Group.objects.get_or_create(name='Менеджеры')

        # Настраиваем права
        self.setup_user_permissions(user_group)
        self.setup_manager_permissions(manager_group)

        self.stdout.write(self.style.SUCCESS('Права доступа успешно обновлены'))

    def setup_manager_permissions(self, group):
        """Расширенные права для менеджеров"""
        # Просмотр всех объектов
        self.add_model_permissions(group, Client, ['view'])
        self.add_model_permissions(group, Mailing, ['view'])
        self.add_model_permissions(group, Message, ['view'])
        self.add_model_permissions(group, User, ['view'])  # Просмотр пользователей

        # Специальные права
        custom_perms = [
            ('auth', 'can_block_user'),  # Блокировка пользователей
            ('messaging', 'can_disable_mailing'),  # Отключение рассылок
            ('messaging', 'can_view_all_mailings'),  # Просмотр всех рассылок
            ('messaging', 'can_view_user_stats'),  # Просмотр статистики по пользователям
        ]

        for app_label, codename in custom_perms:
            self.add_custom_permission(group, app_label, codename)
