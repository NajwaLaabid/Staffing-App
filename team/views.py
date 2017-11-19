from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Employee
from dashboard.models import Project, Resources, ProjectCalendar
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from collections import OrderedDict

def index(request):
    employees = Employee.objects.all()
    total_hours = 0
    total_hours_month = 0
    max_hours_month = 0
    employees_info = []
    h_ratio = 0

    for employee in employees:
        resources = Resources.objects.filter(Employee=employee)
        for resource in resources:#get hours for current month for all projects
            project_calendar = ProjectCalendar.objects.filter(Employee=employee, Project=resource.Project)
            for month in project_calendar: #get hours of current month
                if datetime.now().strftime('%b') == month.date.split('-')[0]:
                    total_hours_month += month.hours
                    max_hours_month = month.max_hours
                total_hours += month.hours

        employee.employee_totalHours = total_hours

        if max_hours_month != 0:
            h_ratio = (total_hours_month / max_hours_month) * 100

        if total_hours_month < 200:
            css_class = 'progress-bar progress-bar-red progress-bar-striped'
            employee.employee_status = 'UC'
        elif total_hours_month == 200:
            css_class = 'progress-bar progress-bar-green progress-bar-striped'
            employee.employee_status = 'NC'
        else:
            css_class = 'progress-bar progress-bar-yellow-perso  progress-bar-striped'
            employee.employee_status = 'OC'

        employee.save()

        employee_i = {'employee' : employee, 'h_ratio' : h_ratio, 'hours_month' : total_hours_month, 'max_hours' : max_hours_month, 'total_hours_month' : total_hours_month, 'css_class' : css_class}
        employees_info.append(employee_i)

    return TemplateResponse(request, 'teamIndex.html', {'employees_info': employees_info})

def viewDepartments(request):
    return TemplateResponse(request, 'departments.html')

def addProject(request, employee_ID):
   if request.method == 'POST':
        potential_project = request.POST['potential_project']
        #potential_project = 1
        r = Resources(Employee=Employee.objects.get(employee_ID=employee_ID)
                    , Project=Project.objects.get(project_ID=potential_project))
        r.save()
        return HttpResponseRedirect('/team/viewEmployee/'+ employee_ID)

def deleteProject(request, employee_ID):
    if request.method == 'POST':
        project_ID = request.POST['project_ID']
        Resources.objects.get(Employee=Employee.objects.get(employee_ID=employee_ID), Project=Project.objects.get(project_ID=project_ID)).delete()
        return HttpResponseRedirect('/team/viewEmployee/'+ employee_ID)

def daterange(dates):
    #start, end = [datetime.strptime(_, "%m/%d/%Y") for _ in dates]
    return OrderedDict(((dates[0] + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((dates[1] - dates[0]).days)).keys()

def viewEmployee(request, employee_ID):
    employee = Employee.objects.get(pk=employee_ID)
    potential_projects = Project.objects.all()
    resources = Resources.objects.filter(Employee=employee)
    projects_with_dates = []

    for resource in resources:
        potential_projects = potential_projects.exclude(project_ID=resource.Project.project_ID)
        #get dates interval of projects of employee
        dates = [resource.Project.start_date, resource.Project.end_date]
        date_range = list(daterange(dates))

        #project_calendar contains all the months span of the project, with hours for every month
        project_calendar = ProjectCalendar.objects.filter(Employee=employee, Project=resource.Project.project_ID)
        hours_per_month = []
        #get hours for every month, and put in json object with date
        for d in date_range:
            for month in project_calendar:
                if d == month.date:
                    h_month = {'hours_month' : month.hours, 'max_hours' : month.max_hours}
                    hours_per_month.append(h_month)

        project_tuple = (resource.Project, date_range, hours_per_month)
        projects_with_dates.append(project_tuple)

    return TemplateResponse(request, 'teamDetails.html', {'employee' : employee, 'potential_projects' : potential_projects, 'resources' : resources, 'projects_with_dates' : projects_with_dates},)

def getEmployeeStatus(request):
    statuses = Employee.objects.all()
    return TemplateResponse(request, 'teamIndex.html', {'employees': employees,})

def addEmployee(request):
    #if not request.user.is_authenticated():
     #   return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        # ADD TO DB
        employee = Employee.objects.create(employee_code = request.POST['employee_code']
        , employee_firstName = request.POST['employee_firstName']
        , employee_lastName = request.POST['employee_lastName']
        , employee_email = request.POST['employee_email']
        , employee_phoneNumber = request.POST['employee_phoneNumber']
        , employee_role = request.POST['employee_role']
        , employee_status = 'UC' #initially all employees undercharge
        , employee_totalHours = 0)

        employee.save()
        return HttpResponseRedirect('/team')
    return TemplateResponse(request, 'addEmployee.html',{})

def deleteEmployee(request, employee_ID):
    Employee.objects.get(pk=employee_ID).delete()

    return HttpResponseRedirect('/team/')


def updateEmployee(request, employee_ID):
    if request.method == 'POST':
        # ADD TO DB
        employee = Employee.objects.get(employee_ID=employee_ID)
        employee.employee_code = request.POST['employee_code']
        employee.employee_firstName = request.POST['employee_firstName']
        employee.employee_lastName = request.POST['employee_lastName']
        employee.employee_email = request.POST['employee_email']
        employee.employee_phoneNumber = request.POST['employee_phoneNumber']
        employee.employee_role = request.POST['employee_role']
        employee.save()

        return HttpResponseRedirect('/team')

    employee = Employee.objects.get(employee_ID=employee_ID)
    return TemplateResponse(request, 'updateEmployee.html', {'employee' : employee},)
