from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from .forms import SignUpForm, LoginForm

def signup(request):
    error_message = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_name = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            if not User.objects.filter(email=user_email).exists():
                if not User.objects.filter(username=user_name).exists():
                    form.save()
                    user = authenticate(username=user_name, password=user_password, email=user_email)
                    dj_login(request, user)
                    return HttpResponseRedirect('/team/viewDepartments')
                else:
                    error_message = "username already exist"
            else:
                error_message = "email already exist"
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

def login(request):
    if request.method == 'POST':
        # form = LoginForm(request.POST)
        # user = form.login(request.POST)
        message = ""
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            dj_login(request, user)
            return HttpResponseRedirect('/team/viewDepartments')# Redirect to a success page.
        else:
            message = "Invalid credentials"
            return render(request, 'login.html', {"message" : message})
    # else:
    #     form = LoginForm()
    return render(request, 'login.html', )

def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/profiles/login')

def resetpassword(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_new_password = request.POST['user_new_password']
        user = authenticate(username=username, password=password)
        if user:
            user.set_password(user_new_password)
            user.save()
            dj_login(request, user)
            return HttpResponseRedirect('/team/viewDepartments')# Redirect to a success page.
        else:
            message = "Invalid credentials"
            return render(request, 'resetpassword.html', {"message" : message})
    return render(request, 'resetpassword.html', {"message" : message})
