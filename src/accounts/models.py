from django.db import models

# Create your models here.

from django.contrib.auth.models import Group

# Create groups for different user roles
free_user_group, created = Group.objects.get_or_create(name='FreeUser')
premium_user_group, created = Group.objects.get_or_create(name='PremiumUser')
manager_group, created = Group.objects.get_or_create(name='Manager')
admin_group, created = Group.objects.get_or_create(name='Admin')
