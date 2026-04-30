from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Profile

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        data = sociallogin.account.extra_data

        if sociallogin.account.provider == 'google':
            first_name = data.get('given_name', '')
            last_name = data.get('family_name', '')

        elif sociallogin.account.provider == 'github':
            full_name = data.get('name', '')
            if full_name:
                parts = full_name.split(' ', 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''
            else:
                first_name = data.get('login', '')
                last_name = ''

        else:
            first_name = ''
            last_name = ''

        Profile.objects.update_or_create(
            user=user,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        return user