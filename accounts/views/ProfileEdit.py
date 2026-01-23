from django.shortcuts import render, redirect
from accounts.forms import ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form})