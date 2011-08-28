from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from accounts.models import Subscription, Receipt
import datetime


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    """ Total number of users """
    @staticmethod
    def total_users():
        return User.objects.count()
    
    ''' Average signups per day/week/month '''
    @staticmethod
    def average_signups():
        today = datetime.date.today()
        daily = Subscription.objects.filter(
            date_created__day=today.day, 
            date_created__month=today.month, 
            date_created__year=today.year
        ).count()
        
        before_week = today - datetime.timedelta(days=7)
        weekly = Subscription.objects.filter(date_created__gt=before_week).count()
        
        before_month = today - datetime.timedelta(days=30)
        monthly = Subscription.objects.filter(date_created__gt=before_month).count()
        
        return '%d / %d / %d' % (daily, weekly, monthly)
    
    ''' Churn rage per day '''
    @staticmethod
    def left_daily():
        today = datetime.date.today()
        return Subscription.objects.filter(
            date_cancelled__day=today.day, 
            date_cancelled__month=today.month, 
            date_cancelled__year=today.year,
            date_deleted__day=today.day, 
            date_deleted__month=today.month, 
            date_deleted__year=today.year
        ).count()
        
    ''' Churn rage per week '''
    @staticmethod
    def left_weekly():
        before_week = datetime.date.today() - datetime.timedelta(days=7)
        return Subscription.objects.filter(
            date_cancelled__gt=before_week,
            date_deleted__gt=before_week
        ).count()
    
    ''' Churn rage per month '''
    @staticmethod
    def left_monthly():
        before_month = datetime.date.today() - datetime.timedelta(days=30)
        return Subscription.objects.filter(
            date_cancelled__gt=before_month,
            date_deleted__gt=before_month
        ).count()
        
    ''' Churn rage per day/week/month (churn = people who left the service) '''
    @staticmethod
    def churn_rage_per_time():
        return '%d / %d / %d' % (Dashboard.left_daily(), Dashboard.left_weekly(), Dashboard.left_monthly())
    
    ''' Churn to acquisition ratio '''
    @staticmethod
    def churn_acquisition():
        acquired = User.objects.filter(is_active=1).count()
        return ('%d%% / %d%% / %d%%' % (
                Dashboard.left_daily()/acquired*100, 
                Dashboard.left_weekly()/acquired*100, 
                Dashboard.left_monthly()/acquired*100)) if acquired != 0 else '0% / 0% / 0%'
    
    ''' Number of users who did not access the service in more than a week/month (% and number) '''
    @staticmethod
    def not_access_users():
        now = datetime.datetime.now()
        week_count = User.objects.filter(last_login__gt=now - datetime.timedelta(days=7)).count()
        month_count = User.objects.filter(last_login__gt=now - datetime.timedelta(days=30)).count()
        count = User.objects.count()
        return "%d%%(%d) / %d%%(%d)" % (
                week_count/float(count)*100 if count else 0,
                week_count, 
                month_count/float(count)*100 if count else 0, 
                month_count)
    
    ''' Number of users who did not activate their account (% and number) '''
    @staticmethod
    def not_activate_users():
        return User.objects.filter(is_active=0).count()
    
    ''' Average number of files per user '''
    @staticmethod
    def average_files():
        average = Subscription.objects.annotate(files_count=Count('files')
                    ).aggregate(Avg('files_count'))['files_count__avg']                    
        return '%.1f' % (average if average else 0)
    
    ''' Average number of shares per user '''
    @staticmethod
    def average_shares():
        query = 'select id, avg(c) average from (select a.id, count(s.id) c from auth_user a left join shares_share s on s.user_created_id=a.id group by a.id) b'
        average = User.objects.raw(query)[0].average
        return '%.1f' % (average if average else 0)
    
    ''' Average length of a user lifetime (in months) '''
    @staticmethod
    def average_lifetime_in_months():
        query = """select *, from_unixtime(avg(unix_timestamp(date_created))) average 
            from accounts_subscription where date_cancelled is null and date_deleted is null and date_created is not null """
        average = User.objects.raw(query)[0].average
        return '%.1f' % ((datetime.datetime.now() - average).days/30.0 if average else 0)
    
    ''' Average lifetime value of a user (in dollars) '''
    @staticmethod
    def average_lifetime_in_dollars():
        query = 'select id, avg(s) average from (select id, sum(amount) s from accounts_receipt group by user_created_id)a'
        average = Receipt.objects.raw(query)[0].average
        return '%.2f' % (average if average else 0)
    
    ''' Recurring monthly revenue '''
    @staticmethod
    def monthly_revenue():
        sum = Receipt.objects.filter(
                date_created__month=datetime.date.today().month).aggregate(Sum('amount'))['amount__sum']                
        return '%.2f' % (sum if sum else 0)
        
''' Created to show user count statistics per country '''
class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    
    def user_count(self):
        return "%.1f %%" % (self.count / float(Subscription.objects.count())*100)
    
    
        