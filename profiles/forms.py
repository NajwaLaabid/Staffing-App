from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout

class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text='envelope', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Email'
        }
    ))

    username = forms.CharField(help_text='user', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Username'
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

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(help_text='user', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Username'
        }
    ))

    password = forms.CharField(help_text='lock', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Password'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password')
    
    def login(self, request):
        username = request['username']
        password = request['password']
        '''
        username = "najwa10"
        password = "123"'''
        user = authenticate(username=username, password=password)
        
        return user
