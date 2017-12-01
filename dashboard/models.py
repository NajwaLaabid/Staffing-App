from django.db import models

# Create your models here.
class Project(models.Model):
	project_ID = models.AutoField(primary_key=True)
	project_code = models.CharField(max_length=200, unique=True)
	project_title = models.CharField(max_length=200)
	project_closed = models.BooleanField(default=False)

	# ON_GOING = 'GO'
	# HOLD = 'HO'
	# AT_RISK = 'RI'
	# PROJECT_STATUS = (
    #     (ON_GOING, 'On going'),
    #     (HOLD, 'Hold'),
    #     (AT_RISK, 'At risk'),
    
    # )
	project_status = models.CharField(max_length=200, default='On going')

	# CASE_STUDY = 'CS'
	# CONCEPTUAL = 'CO'
	# BASIC_ENGINEERING = 'BE'
	# DETAILED_ENGINEERING = 'DE'
	# PROJECT_PHASE = (
	# 	(CASE_STUDY, 'Case Study'),
    #     (CONCEPTUAL, 'Conceptual'),
    #     (BASIC_ENGINEERING, 'Basic Engineering'),
    #     (DETAILED_ENGINEERING, 'Detailed Engineering'),
	# )
	project_phase = models.CharField(max_length=200, default='Case Study')

	# EPC = 'EP'
	# PMC = 'PM'
	# EPCM = 'EM'
	# JESA_ROLE = (
	# 	(EPC, 'EPC'),
	# 	(PMC,'PMC'),
	# 	(EPCM, 'EPCM'),
	# )
	jesa_role = models.CharField(max_length=200, default='EPC')

	estimated_hours = models.IntegerField(default=0)

	actual_hours = models.IntegerField(default=0)

	start_date = models.DateTimeField()

	end_date = models.DateTimeField()

class Resources(models.Model):
    Employee = models.ForeignKey('team.Employee')
    Project = models.ForeignKey(Project)
    Implication_Percentage = models.IntegerField(default=0)
    actual_hours = models.IntegerField(default=0)
    estimated_hours = models.IntegerField(default=0)
    class Meta:
        unique_together = ('Employee', 'Project',)

class ProjectCalendar(models.Model):
	Employee = models.ForeignKey('team.Employee')
	Project = models.ForeignKey(Project)
	date = models.CharField(max_length=200)
	max_hours = models.IntegerField(default=200)
	hours = models.IntegerField(default=0)
	class Meta:
		unique_together = ('Employee', 'Project', 'date')

class PossibleDeliverables(models.Model):
	deliverable_ID = models.AutoField(primary_key=True)
	deliverable_title = models.CharField(max_length=200)
	deliverable_main_category = models.CharField(max_length=200, default=None)

class Deliverables(models.Model):
	deliverable_project_ID = models.AutoField(primary_key=True)
	Project = models.ForeignKey(Project, default=None)
	deliverable = models.ForeignKey(PossibleDeliverables, default=None)
	is_done = models.BooleanField(default=False)
	class Meta:
		unique_together = ('Project', 'deliverable')

class Assumption(models.Model):
	assumption_ID = models.AutoField(primary_key=True)
	Project = models.ForeignKey(Project)
	assumption_text = models.CharField(max_length=200)
	class Meta:
		unique_together = ('Project', 'assumption_text')
