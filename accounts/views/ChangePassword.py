from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def change_password(request):
    user = request.user

    FormClass = PasswordChangeForm if user.has_usable_password() else SetPasswordForm

    if request.method == "POST":
        form = FormClass(user, request.POST)
        if form.is_valid():
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)

            if user.has_usable_password():
                messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
            else:
                messages.success(request, "Parolingiz muvaffaqiyatli o'rnatildi! Endi email/password bilan ham kira olasiz.")

            return redirect("profile_view")
    else:
        form = FormClass(user)

    return render(request, "accounts/change_password.html", {
        "form": form,
        "has_password": user.has_usable_password(),
    })
