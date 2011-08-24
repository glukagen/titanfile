from common.models import BaseModel
from django.contrib import admin
from reversion.admin import VersionAdmin

class BaseAdmin(VersionAdmin):
    list_display=('name', 'date_created', 'date_modified', 'is_active')
    #list_filter = ('is_active',)
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ('user_created', 'user_modified')
