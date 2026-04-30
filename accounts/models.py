from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import RegexValidator
from PIL import Image
from django.utils import timezone
from datetime import timedelta
from accounts.utils import generate_token
import os


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex[:10]}.{ext}"
    return f'avatars/{instance.user.id}/{new_filename}'

phone_regex = RegexValidator(regex=r'^\+998\d{9}$',message="Telefon raqami '+998XXXXXXXXX' formatida bo'lishi kerak.")
telegram_id_validator = RegexValidator(regex=r'^\d{5,15}$',message="Telegram ID faqat raqamlardan iborat bo'lishi kerak.")

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True,)
    email = models.EmailField(unique=True,)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True,null=True)
    last_name = models.CharField(max_length=30, blank=True,null=True)
    telegram_id = models.CharField(max_length=15, validators=[telegram_id_validator], blank=True)
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True,null=True,default='avatars/default.png')

    def save(self, *args, **kwargs):
        avatar_changed = False

        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.avatar != self.avatar:
                    avatar_changed = True
                    if old_profile.avatar and old_profile.avatar.name != 'avatars/default.png':
                        if os.path.isfile(old_profile.avatar.path):
                            os.remove(old_profile.avatar.path)
            except Profile.DoesNotExist:
                avatar_changed = True
        else:
            avatar_changed = True

        super().save(*args, **kwargs)

        if avatar_changed and self.avatar:
            if self.avatar.name != 'avatars/default.png':
                try:
                    img = Image.open(self.avatar.path)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(self.avatar.path)
                except Exception as e:
                    print(f"Rasmga ishlov berishda xato: {e}")

    def __str__(self):
        return self.user.username

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'code')

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=2)
        return timezone.now() <= expiration_time and not self.is_used

    def __str__(self):
        return f"{self.user.username} - {self.code}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(minutes=10)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_token()
        super().save(*args, **kwargs)