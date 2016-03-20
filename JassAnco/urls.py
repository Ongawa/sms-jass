from django.conf.urls import patterns, include, url
from django.contrib import admin
from JassAnco import *

urlpatterns = patterns('',
    url(r'^go/', include(admin.site.urls)),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'},name = 'login'), 
    url(r'^close/$', 'django.contrib.auth.views.logout_then_login', name = 'logout'), 


    url(r'^admin/$','Data.views.admin', name = 'admin'),
    url(r'^send/$','Data.views.send', name = 'send'),
    url(r'^list_pay/$','Data.views.list_pay', name = 'list_pay'),
    url(r'^new_message/$','Data.views.new_message', name = 'new_message'),
    #url(r'^login/$','Data.views.login', name = 'login'),
    url(r'^$','Data.views.home', name = 'home'),
    url(r'^search_reservoir/$','Data.views.search_reservoir', name = 'search_reservoir'),
    url(r'^search_measurement/$','Data.views.search_measurement', name = 'search_measurement'),
    url(r'^search_measurement_graf/$','Data.views.search_measurement_graf', name = 'search_measurement_graf'),
    url(r'^map/$','Data.views.map', name = 'map'),
    url(r'^send_msg/$','Data.views.send_msg', name = 'send_msg'),
    url(r'^pie/$','Data.views.pie', name = 'pie'),
    url(r'^guide/$','Data.views.guide', name = 'guide'),
    url(r'^help/$','Data.views.help', name = 'help'),
)
