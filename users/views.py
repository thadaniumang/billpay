from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Registration Page for USer Creation
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Account has been created, you will now be able to Log In')
            return redirect('site-sign-in')
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Create an Account',
        'form': form
    }
    return render(request, 'users/register.html', context)


# Profile Page to view and edit account details
@login_required
def account(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your Account has been Updated')
            return redirect('site-account')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Account',
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'users/account.html', context)
