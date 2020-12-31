from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Preference


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        print('creating')
        preference = Preference(owner=instance.username)
        preference.save()
        profile = Profile(user=user, preference=preference)
        profile.save()
