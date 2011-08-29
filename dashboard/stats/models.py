from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from accounts.models import Subscription, Receipt
import datetime


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    @staticmethod
    def total_users():
        """ Total number of users """
        return User.objects.count()
    
    @staticmethod
    def average_signups():
        ''' Average signups per day/week/month '''
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
    
    @staticmethod
    def left_daily():
        ''' Churn rage per day '''
        today = datetime.date.today()
        return Subscription.objects.filter(
            date_cancelled__day=today.day, 
            date_cancelled__month=today.month, 
            date_cancelled__year=today.year,
            date_deleted__day=today.day, 
            date_deleted__month=today.month, 
            date_deleted__year=today.year
        ).count()
        
    @staticmethod
    def left_weekly():
        ''' Churn rage per week '''
        before_week = datetime.date.today() - datetime.timedelta(days=7)
        return Subscription.objects.filter(
            date_cancelled__gt=before_week,
            date_deleted__gt=before_week
        ).count()
    
    
    @staticmethod
    def left_monthly():
        ''' Churn rage per month '''
        before_month = datetime.date.today() - datetime.timedelta(days=30)
        return Subscription.objects.filter(
            date_cancelled__gt=before_month,
            date_deleted__gt=before_month
        ).count()
        
    
    @staticmethod
    def churn_rage_per_time():
        ''' Churn rage per day/week/month (churn = people who left the service) '''
        return '%d / %d / %d' % (Dashboard.left_daily(), Dashboard.left_weekly(), Dashboard.left_monthly())
    
    @staticmethod
    def churn_acquisition():
        ''' Churn to acquisition ratio '''
        acquired = User.objects.filter(is_active=1).count()
        return ('%d%% / %d%% / %d%%' % (
                Dashboard.left_daily()/acquired*100, 
                Dashboard.left_weekly()/acquired*100, 
                Dashboard.left_monthly()/acquired*100)) if acquired != 0 else '0% / 0% / 0%'
    
    @staticmethod
    def not_access_users():
        ''' Number of users who did not access the service in more than a week/month (% and number) '''
        now = datetime.datetime.now()
        week_count = User.objects.filter(last_login__gt=now - datetime.timedelta(days=7)).count()
        month_count = User.objects.filter(last_login__gt=now - datetime.timedelta(days=30)).count()
        count = User.objects.count()
        return "%d%%(%d) / %d%%(%d)" % (
                week_count/float(count)*100 if count else 0,
                week_count, 
                month_count/float(count)*100 if count else 0, 
                month_count)
    
    @staticmethod
    def not_activate_users():
        ''' Number of users who did not activate their account (% and number) '''
        return User.objects.filter(is_active=0).count()
    
    @staticmethod
    def average_files():
        ''' Average number of files per user '''
        average = Subscription.objects.annotate(files_count=Count('files')
                    ).aggregate(Avg('files_count'))['files_count__avg']                    
        return '%.1f' % (average if average else 0)
    
    @staticmethod
    def average_shares():
        ''' Average number of shares per user '''
        query = 'select id, avg(c) average from (select a.id, count(s.id) c from auth_user a left join shares_share s on s.user_created_id=a.id group by a.id) b'
        average = User.objects.raw(query)[0].average
        return '%.1f' % (average if average else 0)
    
    @staticmethod
    def average_lifetime_in_months():
        ''' Average length of a user lifetime (in months) '''
        query = """select *, from_unixtime(avg(unix_timestamp(date_created))) average 
            from accounts_subscription where date_cancelled is null and date_deleted is null and date_created is not null """
        average = User.objects.raw(query)[0].average
        return '%.1f' % ((datetime.datetime.now() - average).days/30.0 if average else 0)
    
    @staticmethod
    def average_lifetime_in_dollars():
        ''' Average lifetime value of a user (in dollars) '''
        query = 'select id, avg(s) average from (select id, sum(amount) s from accounts_receipt group by user_created_id)a'
        average = Receipt.objects.raw(query)[0].average
        return '%.2f' % (average if average else 0)
    
    @staticmethod
    def monthly_revenue():
        ''' Recurring monthly revenue '''
        sum = Receipt.objects.filter(
                date_created__month=datetime.date.today().month).aggregate(Sum('amount'))['amount__sum']                
        return '%.2f' % (sum if sum else 0)
        

class Country(models.Model):
    ''' Created to show user count statistics per country '''
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    
    def user_count(self):
        return "%.1f %%" % (self.count / float(Subscription.objects.count())*100)
    
    
        