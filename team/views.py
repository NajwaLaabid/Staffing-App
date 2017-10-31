from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Employee
from dashboard.models import Project
from dashboard.models import Resources

def index(request):
    employees = Employee.objects.all()
    return TemplateResponse(request, 'teamIndex.html', {'employees': employees,})

def viewEmployee(request, employee_ID):
    employee = Employee.objects.get(pk=employee_ID)
    projects = Project.objects.all()
    resources = Resources.objects.get(Employee=employee_ID).select_related()
    return render(request, 'teamDetails.html', {'employee' : employee}, {'projects' : projects}, {'resources' : resources},)

def getEmployeeStatus(request):
    statuses = Employee.objects.all()
    return TemplateResponse(request, 'teamIndex.html', {'employees': employees,})

def addEmployee(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        '''employee_code = request.POST['employee_code']
        employee_firstName = request.POST['employee_firstName']
        employee_lastName = request.POST['employee_lastName']
        employee_email = request.POST['employee_email']
        employee_phoneNumber = request.POST['employee_phoneNumber']
        employee_status = request.POST['employee_status']
        employee_totalHours = request.POST['employee_totalHours']'''

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

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
def deleteEmployee(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        member_id = request.POST['member_id']

        # TO BE REMOVED, DATA to be saved in DB
        print(member_id)

        return render(request, 'team_list.html', {})

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
