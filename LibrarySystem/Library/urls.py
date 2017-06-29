from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Library.views.HomePage', name = 'HomePage'),
    url(r'^Login/$', 'Library.views.Login', name = 'Login'),
    url(r'^Register/$', 'Library.views.Register', name = 'Register'),
    url(r'^ReaderInfo/$', 'Library.views.ReaderInfo', name = 'ReaderInfo'),
    url(r'^Logout/$', 'Library.views.Logout', name = 'Logout'),
    url(r'^BorrowBookPage/$', 'Library.views.BorrowBookPage', name = 'BorrowBookPage'),
    url(r'^BorrowBook/$', 'Library.views.BorrowBook', name = 'BorrowBook'),
    url(r'^ModifyData/$', 'Library.views.ModifyData', name = 'ModifyData'),
    url(r'^MyBook/$', 'Library.views.MyBook', name = 'MyBook'),
    url(r'^ReturnBookPage/$', 'Library.views.ReturnBookPage', name = 'ReturnBookPage'),
    url(r'^BeginReturnPage/$', 'Library.views.BeginReturnPage', name = 'BeginReturnPage'),
    url(r'^ReturnBook/$', 'Library.views.ReturnBook', name = 'ReturnBook'),
    url(r'^UserCheck/$', 'Library.views.UserCheck', name = 'UserCheck'),

)
