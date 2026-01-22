from django.shortcuts import render ,redirect , get_object_or_404
from accounts.forms import RegisterForm
from accounts.models import CustomUser , OTP
from accounts.tasks import mail_task
from accounts.utils import generate_otp


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        otp_code = generate_otp()
        mail_task.delay(user.id,otp_code)
        OTP.objects.create(user=user,code=otp_code)
        return redirect('/')
    else:
        form = RegisterForm()
        context = {'form':form}
        return render(request,'accounts/register.html',context)



