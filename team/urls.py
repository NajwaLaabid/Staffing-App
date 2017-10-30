from django.conf.urls import url

from . import views

app_name = 'team'
urlpatterns =  [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.addEmployee, name='addEmployee'),
    url(r'^delete/$', views.deleteEmployee, name='deleteEmployee'),
]
