from django.conf.urls import url

from . import views

app_name = 'profiles'
urlpatterns =  [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
]
