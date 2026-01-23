from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import OTP, CustomUser


def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    if request.method == 'POST':
        attempts = request.session.get('otp_attempts', 0)
        if attempts >= 5:
            messages.error(request, "Juda ko'p xato urinish! Iltimos, 15 daqiqadan keyin qayta urinib ko'ring.")
            return render(request, 'accounts/verify_otp.html')

        otp_input = request.POST.get('otp_code')
        otp_obj = OTP.objects.filter(user_id=user_id, code=otp_input, is_used=False).last()

        if otp_obj and otp_obj.is_valid():
            otp_obj.is_used = True
            otp_obj.save()

            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
            request.session.pop('user_id', None)
            request.session.pop('otp_attempts', None)

            messages.success(request, "Profilingiz faollashtirildi!")
            return redirect('login')
        else:
            request.session['otp_attempts'] = attempts + 1
            messages.error(request, f"Kod xato. Qolgan urinishlar: {5 - (attempts + 1)}")

    return render(request, 'accounts/verify_otp.html')