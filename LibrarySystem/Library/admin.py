# -*- coding: utf-8 -*-
from django.contrib import admin
from Library.models import *
# Register your models here.
class ListAdmin(admin.ModelAdmin):
    pass
admin.site.register(List, ListAdmin)
