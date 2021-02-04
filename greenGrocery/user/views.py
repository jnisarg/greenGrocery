from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils.http import is_safe_url

from .models import GuestEmail

# Create your views here.


def guest_register_view(request):
    guest_form = forms.GuestForm(request.POST or None)

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if guest_form.is_valid():
        print(guest_form)
        email = guest_form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        request.session['guest_email'] = new_guest_email.email
        print(redirect_path)
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect(reverse('user:register'))

    context = {
        'guest_form': guest_form
    }

    return render(request, 'user/guest-register.html', context)


def loginView(request):

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    else:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        print(redirect_path)

        if request.method == 'POST':
            login_form = forms.LoginForm()

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    try:
                        del request.session['guest_email_id']
                    except:
                        pass
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
                    else:
                        return redirect(reverse('index'))
            else:
                messages.error(request, 'Invalid Username or Password...')
                return redirect(reverse('user:login'))

        else:
            login_form = forms.LoginForm()

        my_dict = {
            'login_form': login_form,
            'btn': 'login',
        }
        return render(request, 'user/login.html', my_dict)


@login_required
def logoutView(request):
    logout(request)
    return redirect('index')


def registerView(request):

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    else:
        if request.method == 'POST':

            user_form = forms.UserForm(data=request.POST)
            user_profile_info_form = forms.UserProfileInfoForm(
                data=request.POST)

            if user_form.is_valid() and user_profile_info_form.is_valid():

                user = user_form.save()
                user.set_password(user.password)  # hashing password
                user.save()

                profile = user_profile_info_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(
                    request, "Registered Successfully. Login to continue...")
                return redirect(reverse('user:login'))

            else:
                print(user_form.errors, user_profile_info_form.errors)

        else:
            user_form = forms.UserForm()
            user_profile_info_form = forms.UserProfileInfoForm()

        dict = {
            'user_form': user_form,
            'user_profile_info_form': user_profile_info_form
        }

        return render(request, 'user/register.html', dict)
