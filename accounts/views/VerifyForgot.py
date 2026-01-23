from django.shortcuts import render ,redirect , get_object_or_404
from accounts.models import PasswordResetToken
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def reset_password_confirm(request, token):
    reset_obj = get_object_or_404(PasswordResetToken, token=token)

    if not reset_obj.is_valid():
        messages.error(request, "Havola muddati tugagan yoki allaqachon ishlatilgan.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Parollar mos kelmadi.")
        elif len(password) < 12:
            messages.error(request, "Parol juda qisqa (kamida 12 ta belgi bo'lishi kerak).")
        else:
            user = reset_obj.user
            user.password = make_password(password)
            user.save()
            reset_obj.is_used = True
            reset_obj.save()

            messages.success(request, "Parolingiz muvaffaqiyatli yangilandi. Endi kirishingiz mumkin.")
            return redirect('login')

    return render(request, 'accounts/set_new_password.html', {'token': token})