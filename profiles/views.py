from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_email = form.cleaned_data.get('user_email')
            user_name = form.cleaned_data.get('user_name')
            user_password = form.cleaned_data.get('user_password')
            user = authenticate(username=user_name, password=user_password, email=user_email)
            login(request, user)
            return HttpResponse("the user is login")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def detail(request, user_id):
    return HttpResponse("the user ID %s." % user_id)
