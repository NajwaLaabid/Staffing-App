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
    employee_status = (
        (OVERCHARGED, 'Overcharged'),
        (NORMAL_CHARGE, 'Normal Charge'),
        (UNDERCHARGED, 'Under Charge'),
    )
    employee_totalHours = models.IntegerField()
