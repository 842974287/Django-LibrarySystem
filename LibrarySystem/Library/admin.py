# -*- coding: utf-8 -*-
from django.contrib import admin
from Library.models import *
# Register your models here.
#readonly_fields = ('save_date', 'mod_date',)
class ListAdmin(admin.ModelAdmin):
    readonly_fields = ('BorrowDate',)
    pass
admin.site.register(BorrowList, ListAdmin)

class ReaderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Reader, ReaderAdmin)

class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(LibraryUser, UserAdmin)
