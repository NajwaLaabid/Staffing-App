from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from .models import Project

def index(request):
    projects = Project.objects.all()
    return TemplateResponse(request, 'index.html', {'projects': projects,})

def view(request, project_id):
    return render(request, 'details.html', {})

def deleteMember(request):
    return render(request, 'details.html', {})

def addMember(request):
    return render(request, 'details.html', {})

def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        project_title = request.POST['project_title']
        project_code = request.POST['project_code']
        end_date = datetime.strptime(request.POST['end_date'], '%m/%d/%Y')
        start_date = datetime.strptime(request.POST['start_date'], '%m/%d/%Y')
        actual_hours = request.POST['actual_hours']
        estimate_hours = request.POST['estimate_hours']
        project_phase = request.POST['project_phase']
        jesa_role = request.POST['jesa_role']

        team_names = request.POST.getlist('team_names')

        project = Project(project_code=project_code, project_title=project_title, estimated_hours=estimate_hours, actual_hours=actual_hours, start_date=start_date, end_date=end_date, project_status="GO", project_phase=project_phase, jesa_role=jesa_role)
        project.save()
        # TO BE REMOVED, DATA to be saved in DB
        print(team_names)

        return HttpResponseRedirect('/dashboard')

        # choose where to redirect the user after successul data addition
        #return HttpResponseRedirect('/dashboard')
    return render(request, 'create.html', {})

def close(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':

        project_id = request.POST['project_id']
        Project.objects.filter(project_ID=project_id).delete()

        return HttpResponseRedirect('/dashboard')

    return render(request, 'index.html', {})

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
