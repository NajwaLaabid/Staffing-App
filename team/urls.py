from django.conf.urls import url

from . import views

app_name = 'team'
urlpatterns =  [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.addEmployee, name='addEmployee'),
    url(r'^deleteEmployee/(?P<employee_ID>\d+)/$', views.deleteEmployee, name='deleteEmployee'),
    url(r'^addProject/(?P<employee_ID>\d+)/$', views.addProject, name='addProject'),
    url(r'^deleteProject/(?P<employee_ID>\d+)/$', views.deleteProject, name='deleteProject'),
    url(r'^viewEmployee/(?P<employee_ID>\d+)/$', views.viewEmployee, name='viewEmployee'),
]
