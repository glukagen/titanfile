from shares.models import Share
from django.contrib import admin
from common.admin import BaseAdmin

class ShareAdmin(BaseAdmin):
    #list_display = BaseAdmin.list_display + ('email', 'hits', 'verify_recipient', 'verify_phone', 'password')
    list_display = BaseAdmin.list_display + ('email', 'hits', 'verify_phone', 'password')
    raw_id_fields = BaseAdmin.raw_id_fields + ('sender', 'recipient', 'files', 'groups')
    pass

admin.site.register(Share, ShareAdmin)
