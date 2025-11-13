from django.shortcuts import render, redirect
from django.contrib.auth import (login as login_func, logout as logout_func,
                                 authenticate, update_session_auth_hash)
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_func(request, user)
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login_func(request, user)
                return redirect('main')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    logout_func(request)
    return redirect('main')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
