from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Follow
from django.contrib.auth.decorators import login_required

def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Создаем профиль
            return redirect('user_profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  # Перенаправление на страницу со списком постов
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

# def user_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = Profile.objects.get(user=request.user)
#     is_following = Follow.objects.filter(follower=request.user, following=user).exists()
#     return render(request, 'users/profile.html', {'profile': profile, 'is_following': is_following})
@login_required
def follow_user(request):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=request.POST.get('username'))
        if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
            Follow.objects.create(follower=request.user, following=user_to_follow)
        return redirect('user_profile', username=user_to_follow.username)

@login_required
def unfollow_user(request):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, username=request.POST.get('username'))
        follow_relation = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follow_relation.exists():
            follow_relation.delete()
        return redirect('user_profile', username=user_to_unfollow.username)