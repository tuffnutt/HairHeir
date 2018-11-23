from django.contrib import admin
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^(?P<freelancer_id>[0-9]+)$', views.freelancer, name='freelancer'),

    url(r'^client/(?P<client_id>[0-9]+)$', views.client, name='client'),
]