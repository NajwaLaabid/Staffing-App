from django.contrib import admin

from .models import Project, Delivrables, Resources, ProjectCalendar

admin.site.register(Project)
admin.site.register(Delivrables)
admin.site.register(Resources)
admin.site.register(ProjectCalendar)
