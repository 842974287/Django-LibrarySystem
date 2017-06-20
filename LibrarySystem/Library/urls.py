from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Library.views.HomePage', name = 'HomePage'),
    url(r'^submit/$', 'Library.views.Submit', name = 'Submit'),
    url(r'^showlist/$', 'Library.views.ShowList', name = 'ShowList'),
)
