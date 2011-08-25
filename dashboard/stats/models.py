from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from accounts.models import Subscription
import datetime


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)    
    
    @staticmethod
    def total_users():
        return User.objects.count()
    
    @staticmethod
    def average_signups():
        return "average_signups"
    
    @staticmethod
    def churn_rage_per_time():
        return "churn_rage_per_time"
    
    @staticmethod
    def churn_acquisition():
        return "churn_acquisition"
    
    @staticmethod
    def not_access_users():
        now = datetime.datetime.now()
        week_count = User.objects.filter(last_login__lt=now - datetime.timedelta(days=7)).count()
        month_count = User.objects.filter(last_login__lt=now - datetime.timedelta(days=30)).count()
        count = User.objects.count()
        return "%d%%(%d) / %d%%(%d)" % (week_count/float(count)*100, week_count, month_count/float(count)*100, month_count)
    
    @staticmethod
    def not_activate_users():
        return User.objects.filter(is_active=0).count()
    
    @staticmethod
    def average_files():
        return Subscription.objects.annotate(files_count=Count('files')
                    ).aggregate(Avg('files_count'))['files_count__avg']
    
    @staticmethod
    def average_lifetime_in_months():
        date = Subscription.objects.filter(
            is_active=1,
            date_cancelled__isnull=True,
            date_deleted__isnull=True, 
            date_created__isnull=False
            ).aggregate(Avg('date_created'))['date_created__avg']
        date_int = str(int(date))
        delta = datetime.date.today() - datetime.date(int(date_int[:4]), int(date_int[4:6]), int(date_int[6:8]))
        return int(round(delta.days/30.0))

        