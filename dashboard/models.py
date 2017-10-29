from django.db import models

# Create your models here.
class Project(models.Model):
	project_ID = models.AutoField(primary_key=True)
	project_code = model.CharField(max_length=200, unique=True)
	project_title = model.CharField(max_length=200)
	project_status = (
        (ON_GOING, 'On going'),
        (HOLD, 'Hold'),
        (AT_RISK, 'At risk'),
    )
	project_phase = (
		(CASE_STUDY, 'Case Study'),
        (CONCEPTUAL, 'Conceptual'),
        (BASIC_ENGINEERING, 'Basic Engineering'),
        (DETAILED_ENGINEERING, 'Detailed Engineering'),
	)
	jesa_role = (
		(EPC, 'EPC'),
		(PMC,'PMC'),
		(EPCM, 'EPCM'),
	)

	estimated_hours = models.IntegerField()

	actual_hours = models.IntegerField()

	start_date = models.DateTimeField()

	end_date = models.DateTimeField()

	


