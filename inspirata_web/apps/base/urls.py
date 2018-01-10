# """urlconf for the base application"""

from django.conf.urls import url
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
	url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page' : '/'}, name='logout'),
    url(r'^$', tweets, name='tweets'),
    url(r'^start/', start, name='start'),
    url(r'^stop/', stop, name='stop'),
    url(r'^home/$', home, name='home'),
]
