from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType

# Create manager group
manager_group, created = Group.objects.get_or_create(name="Managers")

# Get permissions
content_type = ContentType.objects.get_for_model(User)
view_all = Permission.objects.get(codename="can_view_all")
is_manager = Permission.objects.get(codename="is_manager")

# Add permissions to group
manager_group.permissions.add(view_all, is_manager)

# Assign user to group
user = User.objects.get(email="manager@example.com")
user.groups.add(manager_group)
user.save()
