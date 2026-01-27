from django.shortcuts import redirect ,render
from django.contrib import messages
from accounts.utils import send_message, generate_otp
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required



@login_required
def send_telegram_code(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        if not telegram_id:
            messages.error(request, "Telegram ID kiritilmadi!")
            return redirect('profile_edit')

        otp_code = str(generate_otp())
        message_text = f"Sizning tasdiqlash kodingiz: {otp_code}\nUshbu kod 2 daqiqa davomida amal qiladi."

        try:

            send_message(message_text, telegram_id)

            request.session['tg_verify_code'] = otp_code
            request.session['tg_id_pending'] = telegram_id
            request.session['tg_expire_at'] = (timezone.now() + timedelta(minutes=2)).timestamp()

            messages.info(request, "Kod Telegramingizga yuborildi.")
            return redirect('verify_telegram')
        except Exception:
            messages.error(request, "Kod yuborishda xatolik! Botga /start bosganingizni tekshiring.")

    return redirect('profile_edit')