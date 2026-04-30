from django.contrib import admin

from library.models import Book , Category , Language , BookPurchase


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_at','views_count','is_free','is_active','publisher']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','user']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name','code','is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BookPurchase)
class BookPurchaseAdmin(admin.ModelAdmin):
    list_display = ['user','book','status']