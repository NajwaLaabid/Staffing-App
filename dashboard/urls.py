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
    url(r'^editAssumption/(?P<project_ID>\d+)/(?P<assumption_text>.+)/$', views.editAssumption, name='editAssumption'),
    url(r'^deleteAssumption/(?P<project_ID>\d+)/(?P<assumption_text>.+)/$', views.deleteAssumption, name='deleteAssumption'),
    url(r'^addDeliverable/(?P<project_id>\d+)/$', views.addDeliverable, name='addDeliverable'),
    url(r'^deleteDeliverable/(?P<project_ID>\d+)/(?P<deliverable_pj_ID>\d+)/$', views.deleteDeliverable, name='deleteDeliverable'),
    url(r'^deleteDeliverableGroup/(?P<project_ID>\d+)/(?P<deliv_group>.+)/$', views.deleteDeliverableGroup, name='deleteDeliverableGroup'),
    url(r'^editDeliverableGroup/(?P<project_ID>\d+)/(?P<deliv_group>.+)/$', views.editDeliverableGroup, name='editDeliverableGroup'),
    url(r'^deletePossibleDeliverable/(?P<project_ID>\d+)/(?P<deliv_title>.+)/$', views.deletePossibleDeliverable, name='deletePossibleDeliverable'),
    url(r'^editPossibleDeliverable/(?P<project_ID>\d+)/(?P<deliv_title>.+)/$', views.editPossibleDeliverable, name='editPossibleDeliverable'),
    url(r'^updateDelivrable/(?P<project_id>\d+)/$', views.updateDelivrable, name='updateDelivrable'),
    url(r'^createDeliverable/(?P<project_ID>\d+)/$', views.createDeliverable, name='createDeliverable'),
    url(r'^saveMaxHours/(?P<project_id>\d+)/$', views.saveMaxHours, name='saveMaxHours'),
]
