from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Parol o'zgargandan keyin user tizimdan chiqib ketmasligi uchun:
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
            return redirect('profile_view')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})