from django.conf.urls import url

from . import views

app_name = 'dashboard'
urlpatterns =  [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^close/$', views.close, name='close'),
    url(r'^view/(?P<project_id>\d+)/$', views.view, name='view'),
    url(r'^edit/(?P<project_id>\d+)/$', views.edit, name='edit'),
    url(r'^deleteMember/(?P<project_id>\d+)/$', views.deleteMember, name='deleteMember'),
    url(r'^addMember/(?P<project_id>\d+)/$', views.addMember, name='addMember'),
    url(r'^saveMemberHours/(?P<project_id>\d+)/$', views.saveMemberHours, name='saveMemberHours'),
    url(r'^addAssumption/(?P<project_id>\d+)/$', views.addAssumption, name='addAssumption'),
    url(r'^deleteAssumption/(?P<project_ID>\d+)/$', views.deleteAssumption, name='deleteAssumption'),
    url(r'^updateBudget/(?P<project_id>\d+)/$', views.updateBudget, name='updateBudget'),
    url(r'^addDeliverable/(?P<project_id>\d+)/$', views.addDeliverable, name='addDeliverable'),
     url(r'^deleteDeliverable/(?P<project_ID>\d+)/(?P<deliverable_pj_ID>\d+)/$', views.deleteDeliverable, name='deleteDeliverable'),
    url(r'^updateDelivrable/(?P<project_id>\d+)/$', views.updateDelivrable, name='updateDelivrable'),
    url(r'^saveMaxHours/(?P<project_id>\d+)/$', views.saveMaxHours, name='saveMaxHours'),
]
