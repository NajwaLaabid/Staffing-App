from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Employee
from dashboard.models import Project, Resources, ProjectCalendar
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from collections import OrderedDict
import calendar
from .forms import addEmployeeForm


def index(request):
    employees = Employee.objects.all()
    total_hours = 0
    total_hours_month = 0
    max_hours_month = 0
    employees_info = []
    h_ratio = 0
    hours_left = 0

    for employee in employees:
        total_estimated_hours = 0
        total_hours_month = 0
        #get all projects of employee
        resources = Resources.objects.filter(Employee=employee)
        for resource in resources:#get hours for current month for all projects
            #get estimated hours
            total_estimated_hours += resource.estimated_hours
            hours_left += resource.estimated_hours - resource.actual_hours
            project_calendar = ProjectCalendar.objects.filter(Employee=employee, Project=resource.Project)
            for month in project_calendar: #get hours of current month
                if datetime.now().strftime('%b') == month.date.split('-')[0]:
                    total_hours_month += month.hours
                    max_hours_month = month.max_hours
            employee.employee_hours_month = total_hours_month 

        if max_hours_month != 0:
            h_ratio = (total_hours_month / max_hours_month) * 100
            employee.employee_month_ratio = h_ratio

        if total_hours_month < max_hours_month :
            css_class = 'bg-red'
            employee.employee_status = 'Under-charged'
        elif total_hours_month == max_hours_month:
            css_class = 'bg-green'
            employee.employee_status = 'Normal charge'
        else:
            css_class = 'bg-yellow'
            employee.employee_status = 'Over-charged'

        employee.save()

        employee_i = {'total_estimated_hours': total_estimated_hours,'hours_left': hours_left, 'employee' : employee, 'max_hours' : max_hours_month, 'total_hours_month' : total_hours_month, 'css_class' : css_class}
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    message = ""
    if request.method == 'POST':
        form = addEmployeeForm(request.POST)
        if form.is_valid():
            employees_code = Employee.objects.filter(employee_code= form.cleaned_data['code'])
            employees_email = Employee.objects.filter(employee_email= form.cleaned_data['email'])
            employees_phone = Employee.objects.filter(employee_email= form.cleaned_data['phone'])
            if employees_code:
                message = "Code already used by another employee"
            elif employees_email:
                message = "Email already used by another employee"
            elif employees_phone:
                message = "Phone number already used by another employee"
            else:
                employee = Employee.objects.create(employee_code = form.cleaned_data['code']
                , employee_firstName = form.cleaned_data['fname']
                , employee_lastName = form.cleaned_data['lname']
                , employee_email = form.cleaned_data['email']
                , employee_phoneNumber = form.cleaned_data['phone']
                , employee_role = form.cleaned_data['role']
                , employee_status = 'UC' #initially all employees undercharge
                , employee_totalHours = 0) 

                employee.save()
        
                return HttpResponseRedirect('/team')
    else:
        form = addEmployeeForm()
    return TemplateResponse(request, 'addEmployee.html',{'message' : message, 'form': form})

def deleteEmployee(request, employee_ID):
    Employee.objects.get(pk=employee_ID).delete()

    return HttpResponseRedirect('/team/')


def updateEmployee(request, employee_ID):
    message = ""
    employee = Employee.objects.get(employee_ID=employee_ID)
    if request.method == 'POST':
        form = addEmployeeForm(request.POST)
        if form.is_valid():
            #check if new code is not duplicate
            if employee.employee_code != form.cleaned_data['code']:
                employee_other = Employee.objects.filter(employee_code=form.cleaned_data['code'])
                if employee_other:
                    message = "New code already exists"

            if employee.employee_email != form.cleaned_data['email']:
                employee_other = Employee.objects.filter(employee_email=form.cleaned_data['email'])
                if employee_other:
                    message = "New email already exists"

            if employee.employee_phoneNumber != form.cleaned_data['phone']:
                employee_other = Employee.objects.filter(employee_phoneNumber=form.cleaned_data['phone'])
                if employee_other:
                    message = "New phone already exists"
            if message == '':     
                employee.employee_code = form.cleaned_data['code']
                employee.employee_firstName = form.cleaned_data['fname']
                employee.employee_lastName = form.cleaned_data['lname']
                employee.employee_email = form.cleaned_data['email']
                employee.employee_phoneNumber = form.cleaned_data['phone']
                employee.employee_role = form.cleaned_data['role']
                employee.save()

                return HttpResponseRedirect('/team')
    else:
        form = addEmployeeForm({'code': employee.employee_code, 'fname': employee.employee_firstName, 'lname': employee.employee_lastName, 'email': employee.employee_email, 'phone': employee.employee_phoneNumber, 'role': employee.employee_role})
    
    return TemplateResponse(request, 'updateEmployee.html', {'employee': employee, 'message': message, 'form' : form})
