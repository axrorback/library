from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def enter_telegram_id(request):
    return render(request, 'accounts/enter_telegram_id.html')