from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,min_length=12,max_length=33)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,min_length=12,max_length=33)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')