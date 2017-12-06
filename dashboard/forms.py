from django import forms
from django.forms import ModelChoiceField
from django.core.validators import validate_email
from .models import JesaRoles, Phases, Statuses

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.text

class addProjectForm(forms.Form):
	code = forms.CharField(label="Code", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Project Code'
		}
	))
	title = forms.CharField(label="Title", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Project Title'
		}
	))
	phase = forms.ModelChoiceField(label="Phase", queryset=Phases.objects.all(), widget=forms.Select(
		attrs={
			'class' : 'form-control select2',
			'style' : 'width: 100%;'
		}
	))
	jesa_role = forms.ModelChoiceField(label="JESA Role", queryset=JesaRoles.objects.all(), widget=forms.Select(
		attrs={
			'class' : 'form-control select2',
			'style' : 'width: 100%;'
		}
	))
	status = forms.ModelChoiceField(label="Status", initial="On going", queryset=Statuses.objects.all(), widget=forms.Select(
		attrs={
			'class' : 'form-control select2',
			'style' : 'width: 100%;'
		}
	))
	estimated_hours = forms.CharField(label="Estimated Hours", max_length=200, widget=forms.TextInput(
		attrs={
			'class' : 'form-control',
			'placeholder' : 'Estimated Hours'
		}
	))
	start_date = forms.DateField(label="Start Date", widget=forms.TextInput(
		attrs={
			'class' : 'form-control pull-right',
			'id' : 'start_date'
		}
	))
	end_date = forms.DateField(label="End Date", widget=forms.TextInput(
		attrs={
			'class' : 'form-control pull-right',
			'id' : 'end_date'
		}
	))