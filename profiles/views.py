from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from django.contrib.auth.models import User

from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_name = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            form.save()
            user = authenticate(username=user_name, password=user_password, email=user_email)
            dj_login(request, user)
            return HttpResponseRedirect('/dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                return HttpResponseRedirect('/team/viewDepartments')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/profiles/login')
