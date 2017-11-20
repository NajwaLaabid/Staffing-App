from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from collections import OrderedDict
from django.db.models import Count

from .models import Project, Resources, ProjectCalendar, Assumption, Deliverables, PossibleDeliverables
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

        dates = [project.start_date, project.end_date]
        date_range = list(daterange(dates))

        #max_hours_perMonth = {'Jan' : }

        resources = Resources.objects.filter(Project=project)
        for resource in resources:
            for single_date in date_range:
                if not ProjectCalendar.objects.filter(Employee=resource.Employee, Project=project, date=single_date).exists():
                    c = ProjectCalendar(Employee=resource.Employee, Project=project, date=single_date)
                    c.save()

        return HttpResponseRedirect('/dashboard')

    print(project.start_date)
    return TemplateResponse(request, 'edit.html', {'project': project})

def saveMaxHours(request, project_id):
    if request.method == 'POST':
        max_hours = request.POST['max_hours']
        print(max_hours)
        date = request.POST['date']
        project = Project.objects.get(project_ID=project_id)
        calendars = ProjectCalendar.objects.filter(Project=project, date=date)

        for calendar in calendars:
            calendar.max_hours = max_hours  # change field
            calendar.save() # this will update only

    return HttpResponseRedirect('/dashboard/view/'+ project_id)

def view(request, project_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    project = Project.objects.get(project_ID=project_id)
    resources = Resources.objects.filter(Project=project)
    implication_left = 100
    message = "Member"
    disable = ""
    text_color = ""
    for r in resources:
        implication_left = implication_left - r.Implication_Percentage

    if implication_left <= 0:
        disable = "disabled"
        message = "The total implication of current employees is 100%. You should delete a resource before adding a new one."
        text_color = "text-red"
    assumptions = Assumption.objects.filter(Project=project)
    deliverables = Deliverables.objects.filter(Project=project)
    potential_deliverables = PossibleDeliverables.objects.all()
    deliverables_groups = PossibleDeliverables.objects.values('deliverable_main_category').annotate(dcount=Count('deliverable_main_category'))
    deliverables_per_group = []
    for d in deliverables:
        potential_deliverables = potential_deliverables.exclude(deliverable_title=d.deliverable.deliverable_title)

    #for every group gather the delivs belong to it
    for dg in deliverables_groups:
        groups = {'group': dg['deliverable_main_category']}
        deliv_for_group = []
        for pt_d in potential_deliverables:
            if pt_d.deliverable_main_category == dg['deliverable_main_category']:
                deliv_for_group.append(pt_d)
        groups.update({'deliverables' : deliv_for_group})
        deliverables_per_group.append(groups)

    resources_view = []
    max_hours = []
    isFull = False
    for resource in resources:
        sub = {'name' : resource.Employee.employee_lastName + ' ' + resource.Employee.employee_firstName}
        sub.update({'employee_ID' : resource.Employee.employee_ID})
        sub.update({'total' : resource.actual_hours})
        hours = ProjectCalendar.objects.filter(Project=project, Employee=resource.Employee)
        for hour in hours:
            sub.update({hour.date : hour.hours})
            if not isFull:
                max_hours.append({'date' : hour.date, 'hours' : hour.max_hours})
        isFull = True
        resources_view.append(sub)

    potential_members = Employee.objects.all()

    dates = [project.start_date, project.end_date]
    date_range = list(daterange(dates))

    for resource in resources:
        potential_members = potential_members.exclude(employee_ID=resource.Employee.employee_ID)

    return TemplateResponse(request, 'details.html', {'text_color':text_color,'message': message,'disable': disable,'implication_left': implication_left,'deliverables_per_group':deliverables_per_group, 'project': project, 'deliverables':deliverables, 'resources' : resources, 'resources_view': resources_view, 'assumptions': assumptions, 'potential_members': potential_members, 'date_range': date_range})

def saveMemberHours(request, project_id):
    if request.method == 'POST':
        date = request.POST['date']
        hours = int(request.POST['hours'])
        employee_ID = request.POST['employee_ID']
        project = Project.objects.get(project_ID=project_id)
        employee = Employee.objects.filter(employee_ID=employee_ID)
        pc = ProjectCalendar.objects.get(Project=project, Employee=employee, date=date)
        r = Resources.objects.get(Employee=employee, Project=project)
        if(pc.hours != hours):
            diffHours = hours - pc.hours
            r.actual_hours += diffHours
            project.actual_hours += diffHours
            pc.hours = hours  # change field
            pc.save() # this will update only
            r.save()
            project.save()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def deleteMember(request, project_id):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        print(member_id)
        project = Project.objects.get(project_ID=project_id)
        employee = Employee.objects.get(employee_ID=member_id)
        r = Resources.objects.get(Employee=employee, Project=project)
        project.actual_hours = project.actual_hours - r.actual_hours
        project.save()
        r.delete()
        ProjectCalendar.objects.filter(Project=project, Employee=employee).delete()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addMember(request, project_id):
    if request.method == 'POST':
        potential_member = request.POST['potential_member']
        Implication_Percentage = int(request.POST['Implication_Percentage'])
        project = Project.objects.get(project_ID=project_id)
        employee = Employee.objects.get(employee_ID=potential_member)

        member_estimated_hours = project.estimated_hours * Implication_Percentage / 100

        dates = [project.start_date, project.end_date]

        r = Resources(Employee=employee, Project=project, Implication_Percentage=Implication_Percentage, estimated_hours=member_estimated_hours)
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

def deleteAssumption(request, project_ID):
    if request.method == 'POST':
        assumption_text = request.POST['assumption_text']
        project = Project.objects.get(project_ID=project_ID)
        Assumption.objects.filter(Project=project, assumption_text=assumption_text).delete()

        return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def addDeliverable(request, project_id):
    if request.method == 'POST':
        deliverable = request.POST['deliverable_title']
        deliverable_title_arr = deliverable.split("_")

        project = Project.objects.get(project_ID=project_id)
        delv = PossibleDeliverables.objects.filter(deliverable_title=deliverable_title_arr[1], deliverable_main_category=deliverable_title_arr[0])

        delv_project = Deliverables(Project=project, deliverable=delv[0])
        delv_project.save()

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def updateDelivrable(request, project_id):
    if request.method == 'POST':
        deliverable_ID = request.POST['deliverable_project_ID']
        is_done = False
        if("is_done" in request.POST): is_done = True
        print(is_done)
        project = Project.objects.get(project_ID=project_id)

        delv = Deliverables.objects.get(deliverable_project_ID=deliverable_ID)
        if(delv.is_done != is_done):
            delv.is_done = is_done  # change field
            delv.save() # this will update only

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def deleteDeliverable(request, project_ID, deliverable_pj_ID):
    Deliverables.objects.filter(deliverable_project_ID=deliverable_pj_ID).delete()

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)


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

        project = Project(project_code=project_code, project_title=project_title, estimated_hours=estimate_hours, start_date=start_date, end_date=end_date, project_phase=project_phase, jesa_role=jesa_role)
        project.save()

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
