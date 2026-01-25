from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction

from allauth.socialaccount.signals import social_account_added, social_account_updated

from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def _fill_profile_from_social(sociallogin):
    user = sociallogin.user
    data = (sociallogin.account.extra_data or {})

    first = data.get("given_name") or data.get("first_name") or ""
    last = data.get("family_name") or data.get("last_name") or ""

    if not first and not last:
        name = data.get("name") or ""
        parts = name.split()
        if parts:
            first = parts[0]
            last = " ".join(parts[1:]) if len(parts) > 1 else ""

    profile, _ = Profile.objects.get_or_create(user=user)

    updated = False
    if first and not profile.first_name:
        profile.first_name = first
        updated = True
    if last and not profile.last_name:
        profile.last_name = last
        updated = True

    if updated:
        profile.save(update_fields=["first_name", "last_name"])


@receiver(social_account_added)
def on_social_added(request, sociallogin, **kwargs):
    transaction.on_commit(lambda: _fill_profile_from_social(sociallogin))


@receiver(social_account_updated)
def on_social_updated(request, sociallogin, **kwargs):
    transaction.on_commit(lambda: _fill_profile_from_social(sociallogin))
