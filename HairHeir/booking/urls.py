from django.contrib import admin
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='home'),

    #url(r'^(?P<freelancer_id>[0-9]+)$', views.freelancer, name='freelancer'),

    #url(r'^client/(?P<client_id>[0-9]+)$', views.client, name='client'),

    url(r'^user/(?P<user_id>[0-9]+)$', views.user, name='user'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/client/', views.ClientSignUpView.as_view(), name='client_signup'),
    path('accounts/signup/freelancer/', views.FreelancerSignUpView.as_view(), name='freelancer_signup'),
    path('search/', views.Search, name='search'),
]