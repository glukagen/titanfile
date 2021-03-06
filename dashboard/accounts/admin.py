from accounts.models import Group, UserProfile, Subscription, Plan, Subscription
from django.contrib import admin
from common.admin import BaseAdmin
from reversion.admin import VersionAdmin
#from django.contrib.admin import ModelAdmin as VersionAdmin

class PlanAdmin(VersionAdmin):
    list_display = ('id', 'status', 'name', 'date_activated', 'date_inactivated', 
                    'max_users', 'max_files', 'branding', 'encryption', 'support_type', 'monthly_fee',
                    'user_count')


class GroupAdmin(VersionAdmin):
    list_display = BaseAdmin.list_display + ('account',)


class UserPofileAdmin(VersionAdmin):
    raw_id_fields = BaseAdmin.raw_id_fields + ('user', 'account')
    list_display = BaseAdmin.list_display + ('account',)


class SubscriptionAdmin(VersionAdmin):
    list_display = BaseAdmin.list_display + ('status', 'owner', 'date_expires', 'plan', 'subdomain', )
    #list_filter = BaseAdmin.list_filter + ('status',)


admin.site.register(Plan, PlanAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserProfile, UserPofileAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
