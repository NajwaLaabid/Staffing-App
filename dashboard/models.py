from django.db import models

# Create your models here.
class Project(models.Model):
	project_ID = models.AutoField(primary_key=True)
	project_code = models.CharField(max_length=200, unique=True)
	project_title = models.CharField(max_length=200)

	ON_GOING = 'GO'
	HOLD = 'HO'
	AT_RISK = 'RI'
	PROJECT_STATUS = (
        (ON_GOING, 'On going'),
        (HOLD, 'Hold'),
        (AT_RISK, 'At risk'),
    )
	project_status = models.CharField(max_length=2, choices=PROJECT_STATUS, default='GO')

	CASE_STUDY = 'CS'
	CONCEPTUAL = 'CO'
	BASIC_ENGINEERING = 'BE'
	DETAILED_ENGINEERING = 'DE'
	PROJECT_PHASE = (
		(CASE_STUDY, 'Case Study'),
        (CONCEPTUAL, 'Conceptual'),
        (BASIC_ENGINEERING, 'Basic Engineering'),
        (DETAILED_ENGINEERING, 'Detailed Engineering'),
	)
	project_phase = models.CharField(max_length=1, choices=PROJECT_PHASE, default='CS')

	EPC = 'EP'
	PMC = 'PM'
	EPCM = 'EM'
	JESA_ROLE = (
		(EPC, 'EPC'),
		(PMC,'PMC'),
		(EPCM, 'EPCM'),
	)
	jesa_role = models.CharField(max_length=1, choices=JESA_ROLE, default='EP')

	estimated_hours = models.IntegerField()

	actual_hours = models.IntegerField()

	start_date = models.DateTimeField()

	end_date = models.DateTimeField()

class Resources(models.Model):
    Employee = models.ForeignKey('team.Employee')
    Project = models.ForeignKey(Project)
    Implication_Percentage = models.IntegerField()
    actual_hours = models.IntegerField()
    estimated_hours = models.IntegerField()
    class Meta:
        unique_together = ('Employee', 'Project',)

class Delivrables(models.Model):
	delivrable_ID = models.AutoField(primary_key=True)
	delivrable_title = models.CharField(max_length=200)
	delivrable_main_category = models.CharField(max_length=200)
