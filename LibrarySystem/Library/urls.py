from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Library.views.HomePage', name = 'HomePage'),
    url(r'^Login/$', 'Library.views.Login', name = 'Login'),
    url(r'^Register$', 'Library.views.Register', name = 'Register'),
    url(r'^ReaderInfo$', 'Library.views.ReaderInfo', name = 'ReaderInfo'),
)
