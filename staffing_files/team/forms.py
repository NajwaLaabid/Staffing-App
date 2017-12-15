from django import forms
from django.core.validators import validate_email
from team.choices import ROLES
from .models import EmployeePosition

class addEmployeeForm(forms.Form):
	code = forms.CharField(label="Code", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Employee Code'
		}
	))
	fname = forms.CharField(label="First Name", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Employee First Name'
		}
	))
	lname = forms.CharField(label="Last Name", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Employee Last Name'
		}
	))
	email = forms.EmailField(label="Email", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Employee Email'
		}
	))
	phone = forms.CharField(label="Phone Number", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Employee Phone Number'
		}
	))
	role = forms.ModelChoiceField(label = "Role", queryset=EmployeePosition.objects.all(), widget=forms.Select(
		attrs={
			'class' : 'form-control select2',
			'style' : 'width: 100%;'
		}
	))







