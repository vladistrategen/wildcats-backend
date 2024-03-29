# Generated by Django 4.2.6 on 2024-01-16 17:46

from django.db import migrations
from django.contrib.auth.models import Group

def create_user_groups(apps, schema_editor):
    groups = ['FreeUser', 'PremiumUser', 'Manager', 'Admin']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]
