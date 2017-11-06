from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from collections import OrderedDict

from .models import Project, Resources, ProjectCalendar, Assumption, Deliverables
from team.models import Employee

def daterange(dates):
    #start, end = [datetime.strptime(_, "%m/%d/%Y") for _ in dates]
    return OrderedDict(((dates[0] + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((dates[1] - dates[0]).days)).keys()

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    projects = Project.objects.all()
    return TemplateResponse(request, 'index.html', {'projects': projects})

def edit(request, project_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')

    project = Project.objects.get(project_ID=project_id)

    if request.method == 'POST':
        project_title = request.POST['project_title']
        project_code = request.POST['project_code']
        end_date = datetime.strptime(request.POST['end_date'], '%m/%d/%Y')
        start_date = datetime.strptime(request.POST['start_date'], '%m/%d/%Y')
        estimated_hours = request.POST['estimate_hours']
        project_phase = request.POST['project_phase']
        jesa_role = request.POST['jesa_role']
        project_status = request.POST['project_status']

        if(project.project_title != project_title): project.project_title = project_title  # change field
        if(project.project_code != project_code): project.project_code = project_code  # change field
        if(project.end_date != end_date): project.end_date = end_date  # change field
        if(project.start_date != start_date): project.start_date = start_date  # change field
        if(project.estimated_hours != estimated_hours): project.estimated_hours = estimated_hours  # change field
        if(project.project_phase != project_phase): project.project_phase = project_phase  # change field
        if(project.jesa_role != jesa_role): project.jesa_role = jesa_role  # change field
        if(project.project_status != project_status): project.project_status = project_status  # change field
        project.save() # this will update only

        return TemplateResponse(request, 'edit.html', {'project': project})

    print(project.start_date)
    return TemplateResponse(request, 'edit.html', {'project': project})

def view(request, project_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    project = Project.objects.get(project_ID=project_id)
    resources = Resources.objects.filter(Project=project)
    assumptions = Assumption.objects.filter(Project=project)
    deliverables = Deliverables.objects.filter(Project=project)

    resources_view = []
    for resource in resources:
        sub = {'name' : resource.Employee.employee_lastName + ' ' + resource.Employee.employee_firstName}
        sub.update({'employee_ID' : resource.Employee.employee_ID})
        hours = ProjectCalendar.objects.filter(Project=project, Employee=resource.Employee)
        for hour in hours:
            sub.update({hour.date : hour.hours})
        resources_view.append(sub)

    potential_members = Employee.objects.all()

    dates = [project.start_date, project.end_date]
    date_range = list(daterange(dates))

    for resource in resources:
        potential_members = potential_members.exclude(employee_ID=resource.Employee.employee_ID)

    return TemplateResponse(request, 'details.html', {'project': project, 'deliverables':deliverables, 'resources' : resources, 'resources_view': resources_view, 'assumptions': assumptions, 'potential_members': potential_members, 'date_range': date_range})

def saveMemberHours(request, project_id):
    if request.method == 'POST':
        date = request.POST['date']
        hours = request.POST['hours']
        employee_ID = request.POST['employee_ID']
        project = Project.objects.get(project_ID=project_id)
        employee = Employee.objects.filter(employee_ID=employee_ID)
        pc = ProjectCalendar.objects.get(Project=project, Employee=employee, date=date)
        if(pc.hours != hours):
            pc.hours = hours  # change field
            pc.save() # this will update only
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def deleteMember(request, project_id):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        Resources.objects.get(Employee=Employee.objects.get(employee_ID=member_id), Project=Project.objects.get(project_ID=project_id)).delete()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addMember(request, project_id):
    if request.method == 'POST':
        potential_member = request.POST['potential_member']

        project = Project.objects.get(project_ID=project_id)
        employee = Employee.objects.get(employee_ID=potential_member)

        dates = [project.start_date, project.end_date]

        r = Resources(Employee=employee, Project=project)
        r.save()
        date_range = list(daterange(dates))

        for single_date in date_range:
            c = ProjectCalendar(Employee=employee, Project=project, date=single_date)
            c.save()

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addAssumption(request, project_id):
    if request.method == 'POST':
        assumption_text = request.POST['assumption_text']
        project = Project.objects.get(project_ID=project_id)

        ass = Assumption(Project=project, assumption_text=assumption_text)
        ass.save()

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addDeliverable(request, project_id):
    if request.method == 'POST':
        deliverable_title = request.POST['deliverable_title']
        deliverable_title_arr = deliverable_title.split("_")
        project = Project.objects.get(project_ID=project_id)

        delv = Deliverables(Project=project, deliverable_title=deliverable_title_arr[1], deliverable_main_category=deliverable_title_arr[0])
        delv.save()

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def updateDelivrable(request, project_id):
    if request.method == 'POST':
        deliverable_ID = request.POST['deliverable_ID']
        is_done = False
        if("is_done" in request.POST): is_done = True
        print(is_done)
        project = Project.objects.get(project_ID=project_id)

        delv = Deliverables.objects.get(deliverable_ID=deliverable_ID)
        if(delv.is_done != is_done):
            delv.is_done = is_done  # change field
            delv.save() # this will update only

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
