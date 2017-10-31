from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from .models import Project, Resources
from team.models import Employee

def index(request):
    projects = Project.objects.all()
    return TemplateResponse(request, 'index.html', {'projects': projects})

def view(request, project_id):
    project = Project.objects.get(project_ID=project_id)
    resources = Resources.objects.filter(Project=project)
    potential_members = Employee.objects.all()

    for resource in resources:
        potential_members = potential_members.exclude(employee_ID=resource.Employee.employee_ID)

    return TemplateResponse(request, 'details.html', {'project': project, 'resources': resources, 'potential_members': potential_members})

def deleteMember(request, project_id):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        print(member_id)
        Resources.objects.get(Employee=Employee.objects.get(employee_ID=member_id), Project=Project.objects.get(project_ID=project_id)).delete()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addMember(request, project_id):
    if request.method == 'POST':
        potential_member = request.POST['potential_member']
        r = Resources(Employee=Employee.objects.get(employee_ID=potential_member), Project=Project.objects.get(project_ID=project_id))
        r.save()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        project_title = request.POST['project_title']
        project_code = request.POST['project_code']
        end_date = datetime.strptime(request.POST['end_date'], '%m/%d/%Y')
        start_date = datetime.strptime(request.POST['start_date'], '%m/%d/%Y')
        estimate_hours = request.POST['estimate_hours']
        project_phase = request.POST['project_phase']
        jesa_role = request.POST['jesa_role']

        team_names = request.POST.getlist('team_names')

        project = Project(project_code=project_code, project_title=project_title, estimated_hours=estimate_hours, start_date=start_date, end_date=end_date, project_phase=project_phase, jesa_role=jesa_role)
        project.save()

        for name in team_names:
            r = Resources(Employee=Employee.objects.get(employee_ID=name), Project=project)
            r.save()

        return HttpResponseRedirect('/dashboard')

        # choose where to redirect the user after successul data addition
        #return HttpResponseRedirect('/dashboard')
    employees = Employee.objects.all()
    return render(request, 'create.html', {'employees': employees})

def close(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':

        project_id = request.POST['project_id']
        project = Project.objects.get(project_ID=project_id)
        project.project_closed = True
        project.save()

        return HttpResponseRedirect('/dashboard')

    return render(request, 'index.html', {})

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
