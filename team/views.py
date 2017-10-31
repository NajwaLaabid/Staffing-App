from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Employee
from dashboard.models import Project
from dashboard.models import Resources
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    employees = Employee.objects.all()
    return TemplateResponse(request, 'teamIndex.html', {'employees': employees,})

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

def viewEmployee(request, employee_ID):
    employee = Employee.objects.get(pk=employee_ID)
    potential_projects = Project.objects.all()
    resources = Resources.objects.filter(Employee=employee)
    for resource in resources:
        potential_projects = potential_projects.exclude(project_ID=resource.Project.project_ID)
    
    return TemplateResponse(request, 'teamDetails.html', {'employee' : employee, 'potential_projects' : potential_projects, 'resources' : resources},)

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
        , employee_status = request.POST['employee_status']
        , employee_totalHours = 0)

        employee.save()

    return render(request, 'addEmployee.html', {})

def deleteEmployee(request, employee_ID):
    Employee.objects.get(pk=employee_ID).delete()

    return HttpResponseRedirect('/team/')