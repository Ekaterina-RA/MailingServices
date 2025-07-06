from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from messaging.models import Mailing, Message, Client


class Command(BaseCommand):
    help = 'Create managers group with permissions'

    def handle(self, *args, **options):
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')

        # Добавляем разрешения для просмотра и блокировки
        permissions = [
            'can_view_mailing', 'can_disable_mailing',
            'can_view_message', 'can_disable_message',
            'can_view_client', 'can_block_client',
        ]

        for perm in permissions:
            try:
                if 'mailing' in perm:
                    model = Mailing
                elif 'message' in perm:
                    model = Message
                elif 'client' in perm:
                    model = Client

                permission = Permission.objects.get(
                    content_type__model=model._meta.model_name,
                    codename=perm
                )
                managers_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm} not found'))

        self.stdout.write(self.style.SUCCESS('Successfully created managers group with permissions'))