from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from network.forms import SocialUserCreationForm, SocialUserForm
from network.models import SocialUser


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = SocialUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = SocialUserCreationForm()
    return render(request, 'register.html', {'form': form})


def users_view(request):
    social_users = SocialUser.objects.all()
    return render(request, 'users_view.html', {'social_users': social_users})


def profile_view(request, user_id):
    try:
        social_user = SocialUser.objects.get(id=user_id)
        return render(request, 'profile_view.html', {'social_user': social_user})
    except SocialUser.DoesNotExist:
        return render(request, 'profile_view.html', {'error': 'User not found'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = SocialUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SocialUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def login_is_required(request):
    return render(request, 'login_required.html')