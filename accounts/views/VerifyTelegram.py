from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from accounts.models import Profile
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def verify_telegram(request):
    expire_at = request.session.get('tg_expire_at', 0)
    if not expire_at:
        return redirect('profile_edit')

    if request.method == 'POST':
        user_code = request.POST.get('code')
        session_code = request.session.get('tg_verify_code')

        if timezone.now().timestamp() > expire_at:
            messages.error(request, "Kodning vaqti tugadi!")
            return redirect('profile_edit')

        if user_code == session_code:
            profile = Profile.objects.get(user=request.user)
            profile.telegram_id = request.session.get('tg_id_pending')
            profile.save()

            # Sessiyani tozalash
            request.session.pop('tg_verify_code', None)
            request.session.pop('tg_id_pending', None)
            request.session.pop('tg_expire_at', None)

            messages.success(request, f"Telegram ID ({profile.telegram_id}) muvaffaqiyatli bog'landi!")
            return redirect('profile_view')

        messages.error(request, "Kod xato!")

    return render(request, 'accounts/verify_telegram.html', {'expire_at': expire_at})