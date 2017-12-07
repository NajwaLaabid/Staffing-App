from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from .forms import SignUpForm, LoginForm

def signup(request):
    message = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user_password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']
            if confirm_password == user_password:
                message = "Passwords do not match"
            if not User.objects.filter(username=user).exists():
                    user_obj = User.objects.create_user(user, password=user_password)
                    user = authenticate(username=user, password=user_password)
                    dj_login(request, user)
                    return HttpResponseRedirect('/team/viewDepartments')
            else:
                    message = "Account already exists"
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'message': message})

def login(request):
    message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                dj_login(request, user)
                return HttpResponseRedirect('/team/viewDepartments')# Redirect to a success page.
            else:
                message = "Invalid credentials"
                return render(request, 'login.html', {"form": form, "message" : message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {"form": form, "message" : message})

def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/profiles/login')

def resetpassword(request):
    message = ""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_new_password = form.cleaned_data['user_new_password']
            user = authenticate(username=username, password=password)
            if user:
                user.set_password(user_new_password)
                user.save()
                dj_login(request, user)
                return HttpResponseRedirect('/team/viewDepartments')# Redirect to a success page.
            else:
                message = "Invalid credentials"
                return render(request, 'resetpassword.html', {"form": form, "message" : message})
    
    else:
        form = ResetPasswordForm()
    return render(request, 'resetpassword.html', {"form": form, "message" : message})
