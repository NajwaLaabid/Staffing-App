from django.db import models

# Create your models here.
class Project(models.Model):
	project_ID = models.AutoField(primary_key=True)
	project_code = models.CharField(max_length=200, unique=True)
	project_title = models.CharField(max_length=200)
	project_closed = models.BooleanField(default=False)
	project_status = models.ForeignKey('Statuses', default='')
	project_phase = models.ForeignKey('Phases')
	jesa_role = models.ForeignKey('JesaRoles')
	estimated_hours = models.IntegerField(default=0)
	actual_hours = models.IntegerField(default=0)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

class Resources(models.Model):
	#resource_id = models.AutoField(primary_key=True)
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

class Phases(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return u'{0}'.format(self.text)

class JesaRoles(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return u'{0}'.format(self.text)

class Statuses(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return u'{0}'.format(self.text)