from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil ma’lumotlari'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    list_display = ('username', 'email', 'get_full_name', 'is_staff', 'is_active')
    list_select_related = ('profile',)

    search_fields = ('username', 'email', 'profile__first_name', 'profile__last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy ma’lumotlar', {'fields': ('email',)}),
        ('Huquqlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )

    def get_full_name(self, obj):
        try:
            full_name = f"{obj.profile.first_name} {obj.profile.last_name}".strip()
            return full_name if full_name else obj.username
        except (AttributeError, Profile.DoesNotExist):
            return obj.username

    get_full_name.short_description = 'To‘liq ism'
    get_full_name.admin_order_field = 'profile__first_name'