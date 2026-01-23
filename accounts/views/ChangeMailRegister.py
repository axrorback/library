from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CustomUser, OTP
from accounts.utils import generate_otp
from accounts.tasks import mail_task
from django.utils import timezone

def change_email_and_resend(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Sessiya muddati tugagan.")
        return redirect('register')

    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        new_email = request.POST.get('email')

        if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan.")
        else:
            user.email = new_email
            user.save()

            request.session['user_email'] = new_email
            request.session['last_otp_sent'] = timezone.now().timestamp()
            request.session['otp_attempts'] = 0

            OTP.objects.filter(user=user, is_used=False).update(is_used=True)
            otp_code = generate_otp()
            OTP.objects.create(user=user, code=otp_code)

            mail_task.delay(user.id, otp_code)

            messages.success(request, "Email o'zgartirildi va yangi kod yuborildi.")
            return redirect('verify_otp')

    return render(request, 'accounts/change_email.html', {'user': user})