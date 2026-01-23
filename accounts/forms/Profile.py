from accounts.models import Profile
import os
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'birth_date','telegram_id','phone_number']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            max_size = 2 * 1024 * 1024
            if avatar.size > max_size:
                raise ValidationError("Rasm hajmi 2MB dan oshmasligi kerak!")

            ext = os.path.splitext(avatar.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if ext not in valid_extensions:
                raise ValidationError("Faqat .jpg, .jpeg yoki .png formatidagi rasmlarni yuklashingiz mumkin!")

            try:
                w, h = get_image_dimensions(avatar)
                if not w or not h:
                    raise ValidationError("Yuklangan fayl rasm formatida emas (content error)!")
            except Exception:
                raise ValidationError("Faylni o'qib bo'lmadi. Iltimos, haqiqiy rasm faylini tanlang.")

        return avatar