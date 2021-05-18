from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Congratulations {username}! Your account has been created successfuly. You are now able to login.')
            return redirect('login')                   
    else:
        form = UserRegisterationForm()
        
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form  = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated successfuly.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form  = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)