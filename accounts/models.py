from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import RegexValidator
from PIL import Image
from django.utils import timezone
from datetime import timedelta

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex[:10]}.{ext}"
    return f'avatars/{instance.user.id}/{new_filename}'

username_regex = RegexValidator(regex=r'^[a-zA-Z]{5,20}$',message="Foydalanuvchi nomi 5-20 simvoldan iborat bo'lishi kerak.")
phone_regex = RegexValidator(regex=r'^\+998\d{9}$',message="Telefon raqami '+998XXXXXXXXX' formatida bo'lishi kerak.")
telegram_id_validator = RegexValidator(regex=r'^\d{5,15}$',message="Telegram ID faqat raqamlardan iborat bo'lishi kerak.")
gmail_validator = RegexValidator(regex=r'^[a-zA-Z0-9._%+-]+@gmail\.com$',message="Faqat @gmail.com manzillari qabul qilinadi.")

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, validators=[username_regex])
    email = models.EmailField(unique=True, validators=[gmail_validator])

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=15, validators=[telegram_id_validator], blank=True)
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True,null=True,default='avatars/default.png')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

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
