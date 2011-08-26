from django.contrib import admin
from models import Dashboard, Country
from accounts.models import Subscription
from django.contrib.auth.models import User


class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'calculated')
    
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
        elif dashboard.code  == 'average_shares':
            result = dashboard.average_shares()
        elif dashboard.code == 'average_lifetime_in_months':
            result = dashboard.average_lifetime_in_months() 
        elif dashboard.code == 'average_lifetime_in_dollars':
            result = dashboard.average_lifetime_in_dollars()
        elif dashboard.code =='monthly_revenue':
            result = dashboard.monthly_revenue()       
        return result


class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'count', 'user_count')
    
    def __init__(self, model, admin_site):
        admin.ModelAdmin.__init__(self, model, admin_site)
        
        for c in Country.objects.all():
            s_count = Subscription.objects.filter(country_code=c.code).count()
            if c.count != s_count:
                c.count = s_count
                c.save()
                
        print "test"


admin.site.register(Country, CountryAdmin)
admin.site.register(Dashboard, DashboardAdmin)


