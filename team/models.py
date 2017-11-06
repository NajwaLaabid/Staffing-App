from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_ID = models.AutoField(primary_key=True)
    employee_code = models.CharField(max_length=200, unique=True)
    employee_firstName = models.CharField(max_length=200)
    employee_lastName = models.CharField(max_length=200)
    employee_email = models.EmailField(unique=True)
    employee_phoneNumber = models.CharField(max_length=200, unique=True)
    OVERCHARGED = 'OC'
    NORMAL_CHARGE = 'NC'
    UNDERCHARGED = 'UC'
    STATUSES = (
        (UNDERCHARGED, 'Under Charge'),
        (OVERCHARGED, 'Overcharged'),
        (NORMAL_CHARGE, 'Normal Charge'),
    )
    employee_status = models.CharField(max_length=200, null=True, choices=STATUSES, default=STATUSES[0][0])
    
    ENGINEER = 'EGR'
    DESIGNER = 'DSG'
    ROLES = (
        (ENGINEER, 'EGR'),
        (DESIGNER, 'DSG'),
    )

    employee_role = models.CharField(max_length=200, null=True, choices=ROLES, default=ROLES[0][0])
    employee_totalHours = models.IntegerField(default=0)
