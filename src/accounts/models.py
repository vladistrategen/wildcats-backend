from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# Create groups for different user roles
free_user_group, created = Group.objects.get_or_create(name='FreeUser')
premium_user_group, created = Group.objects.get_or_create(name='PremiumUser')
manager_group, created = Group.objects.get_or_create(name='Manager')
admin_group, created = Group.objects.get_or_create(name='Admin')

@receiver(post_save, sender=User)
def assign_initial_group(sender, instance, created, **kwargs):
    """Assign the user to the 'FreeUser' group after the first signup."""
    if created:
        instance.groups.add(free_user_group)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    #in caz ca e nevoie de numele userului din baza de date
    def __str__(self):
        return self.user.username