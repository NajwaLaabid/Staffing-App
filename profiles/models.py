from django.db import models

class UserTypes(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return u'{0}'.format(self.text)