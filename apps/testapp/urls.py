from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^$', views.index),
    url(r'^reg/$', views.reg),
    url(r'^appointments/$', views.appointments),
    url(r'^logout/$', views.logout),
    url(r'^addtask/$', views.addtask),
    url(r'^login/$', views.login),
]