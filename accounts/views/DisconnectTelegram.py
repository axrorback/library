from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def disconnect_telegram(request):
    if request.method == 'POST':
        profile = request.user.profile
        old_id = profile.telegram_id
        profile.telegram_id = ""
        profile.save()

        messages.success(request, f"Telegram ID ({old_id}) muvaffaqiyatli uzildi.")
        return redirect('profile_view')

    return redirect('profile_view')