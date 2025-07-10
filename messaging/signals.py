from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from messaging.models import Client


@receiver(post_migrate)
def create_manager_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name=settings.MANAGER_GROUP_NAME)
    if created:
        content_type = ContentType.objects.get_for_model(Client)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.set(permissions)
        group.save()
