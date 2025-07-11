from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in ทันทีหลังสมัคร
            return redirect('/')  # เปลี่ยนไปหน้า home หรือ profile ได้
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = getattr(user_profile, 'profile', None)  # Assuming OneToOne Profile
    context = {
        'user_profile': user_profile,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

def about_page(request):
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'privacy.html', {'today': datetime.now().strftime('%d/%m/%Y')})