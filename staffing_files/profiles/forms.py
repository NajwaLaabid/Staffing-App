from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from .models import UserTypes

class SignUpForm(forms.Form):
    user = forms.ModelChoiceField(label="User", queryset=UserTypes.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(help_text='lock', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Password'
        }
    ))

    password2 = forms.CharField(help_text='log-in', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Retype Password'
        }
    ))


class LoginForm(forms.Form):
    username = forms.ModelChoiceField(label="User", queryset=UserTypes.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    password = forms.CharField(help_text='lock', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Password'
        }
    ))

class ResetPasswordForm(forms.Form):
    username = forms.ModelChoiceField(label="User", queryset=UserTypes.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    password = forms.CharField(help_text='lock', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Password'
        }
    ))

    new_password = forms.CharField(help_text='lock', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'New Password'
        }
    ))

