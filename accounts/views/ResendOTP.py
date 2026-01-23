from django.shortcuts import redirect
from accounts.models import CustomUser, OTP
from django.utils import timezone
from accounts.utils import generate_otp
from accounts.tasks import mail_task
from django.contrib import messages

def resend_otp(request):
    user_id = request.session.get('user_id')
    last_sent = request.session.get('last_otp_sent')

    if not user_id:
        return redirect('register')

    if last_sent and (timezone.now().timestamp() - last_sent) < 60:
        messages.warning(request, "Iltimos, bir oz kutib keyin qayta yuboring.")
        return redirect('verify_otp')

    user = CustomUser.objects.get(id=user_id)
    otp_code = generate_otp()

    OTP.objects.filter(user=user, is_used=False).update(is_used=True)
    OTP.objects.create(user=user, code=otp_code)

    mail_task.delay(user.id, otp_code)

    request.session['last_otp_sent'] = timezone.now().timestamp()
    messages.success(request, "Yangi kod yuborildi.")
    return redirect('verify_otp')