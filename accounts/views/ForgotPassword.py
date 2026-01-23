from django.shortcuts import render
from accounts.models import CustomUser, PasswordResetToken
from django.contrib import messages
from accounts.tasks import send_reset



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            reset_obj = PasswordResetToken.objects.create(user=user)
            domain = request.get_host()

            send_reset.delay(user.id, reset_obj.token, domain)

            messages.success(request, "Xavfsiz havola emailingizga yuborildi.")
        else:
            messages.error(request, "Email topilmadi.")

    return render(request, 'accounts/forgot_password.html')