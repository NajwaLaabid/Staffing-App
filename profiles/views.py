from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate
from django.contrib.auth.models import User

from .forms import SignUpForm, LoginForm

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_email = form.cleaned_data.get('user_email')
            user_name = form.cleaned_data.get('user_name')
            user_password = form.cleaned_data.get('user_password')
            user = authenticate(username=user_name, password=user_password, email=user_email)
            login(request, user)
            return HttpResponseRedirect('/profiles/login')
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
                return HttpResponseRedirect('/dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
