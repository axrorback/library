from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('social-auth/',include('allauth.urls')),
    path('payment/',include('billing.urls')),
    path('book/',include('library.urls')),
    path('ckeditor5/',include('django_ckeditor_5.urls')),
]
