from django.shortcuts import render ,redirect
from accounts.forms import RegisterForm
from accounts.models import  OTP
from accounts.tasks import mail_task
from accounts.utils import generate_otp
from django.contrib import messages
from django.utils import timezone


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        OTP.objects.filter(user=user, is_used=False).update(is_used=True)
        otp_code = generate_otp()
        OTP.objects.create(user=user, code=otp_code)

        request.session['user_id'] = str(user.id)
        request.session['otp_attempts'] = 0
        request.session['user_email'] = user.email
        request.session['last_otp_sent'] = timezone.now().timestamp()
        mail_task.delay(user.id, otp_code)

        messages.info(request, "Tasdiqlash kodi emailingizga yuborildi.")
        return redirect('verify_otp')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)