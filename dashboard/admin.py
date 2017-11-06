from django.contrib import admin

from .models import Project, Deliverables, Resources, ProjectCalendar, Assumption

admin.site.register(Project)
admin.site.register(Deliverables)
admin.site.register(Resources)
admin.site.register(ProjectCalendar)
admin.site.register(Assumption)
