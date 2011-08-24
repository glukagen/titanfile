from files.models import File
from django.contrib import admin
from common.admin import BaseAdmin

class FileAdmin(BaseAdmin):
    #list_display = BaseAdmin.list_display + ('hits', 'date_expires')
    list_display = ('name', 'date_created', 'date_expires', 'user_created', 'account', 'hits')
    #list_display = ('hits', 'date_expires')
    #list_display=('name', 'user_created', 'date_created', 'user_modified', 'date_modified', 'is_active')
    #list_display=('name', 'user_created')
    pass

admin.site.register(File, FileAdmin)
