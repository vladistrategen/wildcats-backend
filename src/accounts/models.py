from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def assign_initial_group(sender, instance, created, **kwargs):
    """Assign the user to the 'FreeUser' group after the first signup."""
    if created:
        free_user_group, _ = Group.objects.get_or_create(name='FreeUser')
        instance.groups.add(free_user_group)
