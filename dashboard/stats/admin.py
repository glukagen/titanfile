from django.contrib import admin
from models import Dashboard
from django.contrib.auth.models import User


class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'calculated')
    
    def calculated(self, dashboard):
        result = dashboard.code
        if dashboard.code == 'total_users':
            result = dashboard.total_users()
        elif dashboard.code == 'average_signups':
            result = dashboard.average_signups()        
        elif dashboard.code == 'churn_rage_per_time':
            result = dashboard.churn_rage_per_time()  
        elif dashboard.code == 'churn_acquisition':
            result = dashboard.churn_acquisition()
        elif dashboard.code == 'not_access_users':
            result = dashboard.not_access_users()
        elif dashboard.code == 'not_activate_users':
            result = dashboard.not_activate_users()
        elif dashboard.code == 'average_files':
            result = dashboard.average_files()
        elif dashboard.code == 'average_lifetime_in_months':
            result = dashboard.average_lifetime_in_months()    
        return result


admin.site.register(Dashboard, DashboardAdmin)


