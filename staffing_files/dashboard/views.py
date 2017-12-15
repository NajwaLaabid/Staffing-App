from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from collections import OrderedDict
from django.db.models import Count
from .models import Statuses, JesaRoles, Phases, Project, Resources, ProjectCalendar, Assumption, Deliverables, PossibleDeliverables
from team.models import Employee
from .forms import addProjectForm
import calendar

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
    message = ""

    if request.method == 'POST':
        form = addProjectForm(request.POST)
        if form.is_valid():
            if project.project_code != form.cleaned_data['code']:
                project_other = Project.objects.filter(project_code=form.cleaned_data['code'])
                if project_other:
                    message = "New code already exists"

            if form.cleaned_data['start_date'].isoformat() >= form.cleaned_data['end_date'].isoformat():
                message = "End date should be greater or equal to start date"

            if message == "":
                project.project_title = form.cleaned_data['title']
                project.project_code = form.cleaned_data['code']
                project.end_date = form.cleaned_data['end_date']
                project.start_date = form.cleaned_data['start_date']
                project.estimated_hours = form.cleaned_data['estimated_hours']
                project.project_phase = form.cleaned_data['phase']
                project.jesa_role = form.cleaned_data['jesa_role']
                project.project_status = form.cleaned_data['status']
                
                project.save() # this will update only

                dates = [project.start_date, project.end_date]
                date_range = list(daterange(dates))

                resources = Resources.objects.filter(Project=project)
                for resource in resources:
                    for single_date in date_range:
                        if not ProjectCalendar.objects.filter(Employee=resource.Employee, Project=project, date=single_date).exists():
                            c = ProjectCalendar(Employee=resource.Employee, Project=project, date=single_date)
                            c.save()

                return HttpResponseRedirect('/dashboard')

    else:
        status = Statuses.objects.get(text=project.project_status)
        phase = Phases.objects.get(text=project.project_phase)
        jesa_role = JesaRoles.objects.get(text=project.jesa_role)
        form = addProjectForm({'code': project.project_code, 'title': project.project_title, 'status': status.pk, 'phase': phase.pk, 'jesa_role': jesa_role.pk, 'estimated_hours': project.estimated_hours, 'start_date': project.start_date.date().strftime('%d/%m/%Y'), 'end_date': project.end_date.date().strftime('%d/%m/%Y')})
    
    return TemplateResponse(request, 'edit.html', {'message': message, 'project': project, 'form': form})

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

    #for every group gather the delivs belonging to it
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
    date_coupled_list = []
    nb_dates = len(date_range)
    #get every date coupled with id because zip didn't work in template/inner loop
    for i in range(nb_dates):
        couple = {"n": i, "date" : date_range[i]}
        date_coupled_list.append(couple)

    nb_resources = len(resources_view)

    for resource in resources:
        potential_members = potential_members.exclude(employee_ID=resource.Employee.employee_ID)

    return TemplateResponse(request, 'details.html', {'date_range_coupled':date_coupled_list, 'nb_dates':nb_dates, 'groups': deliverables_groups, 'max_hours' : max_hours, 'text_color':text_color,'message': message,'disable': disable,'implication_left': implication_left,'deliverables_per_group':deliverables_per_group, 'project': project, 'deliverables':deliverables, 'nb_resources' : nb_resources, 'resources_view': resources_view, 'assumptions': assumptions, 'potential_members': potential_members, 'date_range': date_range})

def saveMemberHours(request, project_id, nb_dates):
    if request.method == 'POST':
        for n in range(int(nb_dates)):
            employee_ID = request.POST['employee_ID']
            date = request.POST['date_' + employee_ID + '+' + str(n)]
            hours = int(request.POST[employee_ID + '+' + str(n) + '-form'])
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
        member_id = request.POST['delete_elt_ID']
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
        date_range = list(daterange(dates))
        for single_date in date_range:
            #compute max_hours
            #get month and year
            month_str = single_date.split('-')[0]
            month_nb = list(calendar.month_abbr).index(month_str)
            year_str = single_date.split('-')[1]
            year_str = '20' + year_str
            year_nb = int(year_str)
            #get first day of month and weekday
            weekday_nb = calendar.monthrange(year_nb, month_nb)[0]
            days_in_month = calendar.monthrange(year_nb, month_nb)[1]
            #check if month has 3 mondays
            #days of the week 0 indexed
            if days_in_month == 31 and (weekday_nb == 0 or weekday_nb == 5 or weekday_nb == 6):
                maxHours = 200
            elif days_in_month == 30 and (weekday_nb == 0 or weekday_nb == 6):
                maxHours = 200
            elif days_in_month == 29 and (weekday_nb == 0):
                maxHours = 200
            else:
                maxHours = 160
            c = ProjectCalendar(Employee=employee, Project=project, date=single_date, max_hours=maxHours)
            c.save()

        r.save()
        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def addAssumption(request, project_id):
    if request.method == 'POST':
        assumption_text = request.POST['assumption_text']
        project = Project.objects.get(project_ID=project_id)

        ass = Assumption(Project=project, assumption_text=assumption_text)
        ass.save()

        return HttpResponseRedirect('/dashboard/view/'+ project_id)

def deleteAssumption(request, project_ID):
    if request.method == "POST":
        assumption_ID = request.POST['delete_elt_ID']
        project = Project.objects.get(project_ID=project_ID)
        Assumption.objects.filter(Project=project, assumption_ID=assumption_ID).delete()

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def editAssumption(request, project_ID, assumption_text):
    if request.method == 'POST':
        new_assumption_text = request.POST['assumption_text']
        project = Project.objects.get(project_ID=project_ID)
        Assumption.objects.filter(Project=project, assumption_text=assumption_text).update(assumption_text=new_assumption_text)

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

def deleteDeliverable(request, project_ID):
    if request.method == 'POST':
        deliverable_pj_ID = request.POST['delete_elt_ID']
        Deliverables.objects.filter(deliverable_project_ID=deliverable_pj_ID).delete()

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def deleteDeliverableGroup(request, project_ID):
    if request.method == "POST":
        deliv_group = request.POST['delete_elt_ID']
        PossibleDeliverables.objects.filter(deliverable_main_category=deliv_group).delete()

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def editDeliverableGroup(request, project_ID, deliv_group):
    if request.method == 'POST':
        new_deliv_group = request.POST['deliv_group']
        PossibleDeliverables.objects.filter(deliverable_main_category=deliv_group).update(deliverable_main_category=new_deliv_group)

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def editPossibleDeliverable(request, project_ID, deliv_title):
    if request.method == 'POST':
        new_deliv_title = request.POST['deliv_title']
        PossibleDeliverables.objects.filter(deliverable_title=deliv_title).update(deliverable_title=new_deliv_title)

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)

def deletePossibleDeliverable(request, project_ID):
    if request.method == "POST":
        deliv_ID = request.POST['delete_elt_ID']
        PossibleDeliverables.objects.filter(deliverable_ID=deliv_ID).delete()

    return HttpResponseRedirect('/dashboard/view/'+ project_ID)
    
def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    message = ""
    if request.method == 'POST':
        form = addProjectForm(request.POST)
        if form.is_valid():
            project_title = form.cleaned_data['title']
            project_code = form.cleaned_data['code']
            #check if unique project
            projects = Project.objects.filter(project_code=project_code)
            if projects:
                message = "Project code already exists"
            #check if start and end date correct
            elif form.cleaned_data['start_date'].isoformat() >= form.cleaned_data['end_date'].isoformat():
                message = "End date should be greater or equal to start date"
            else:
                end_date = form.cleaned_data['end_date']
                start_date = form.cleaned_data['start_date']
                estimate_hours = form.cleaned_data['estimated_hours']
                project_phase = form.cleaned_data['phase']
                jesa_role = form.cleaned_data['jesa_role']
                status = form.cleaned_data['status']
                project = Project(project_status=status, project_code=project_code, project_title=project_title, estimated_hours=estimate_hours, start_date=start_date, end_date=end_date, project_phase=project_phase, jesa_role=jesa_role)
                project.save()

                return HttpResponseRedirect('/dashboard')
    else:
        form = addProjectForm()
    employees = Employee.objects.all()
    return render(request, 'create.html', {'form': form, 'message': message, 'employees': employees})

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

def createDeliverable(request, project_ID):
    if request.method == 'POST':
        deliverable_main_category = request.POST['deliverable_group']
        deliverable = request.POST['deliverable']

        PossibleDeliverable = PossibleDeliverables(deliverable_title=deliverable,deliverable_main_category=deliverable_main_category)
        PossibleDeliverable.save()
    
    return HttpResponseRedirect('/dashboard/view/'+ project_ID)