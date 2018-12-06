from django.contrib import admin
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.user, name='user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/client/', views.ClientSignUpView.as_view(), name='client_signup'),
    path('accounts/signup/freelancer/', views.FreelancerSignUpView.as_view(), name='freelancer_signup'),
    path('search/', views.Search, name='search'),
    path('advancedsearch/', views.AdvancedSearch, name='advancedsearch'),
]