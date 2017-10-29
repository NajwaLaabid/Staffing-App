from django.conf.urls import url

from . import views

app_name = 'team'
urlpatterns =  [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^delete/$', views.delete, name='delete'),
]
