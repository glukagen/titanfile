from django.contrib.auth.models import User
from models import Dashboard, Country
from accounts.models import Subscription, Receipt
from files.models import File
from shares.models import Share
import unittest
import datetime
import random
import decimal


''' Test stats Dashboard class methods'''
class DashboardTest(unittest.TestCase):
       
    ''' create and return user with random name '''     
    def getUser(self):
        user = User.objects.create_user("%s%s" %('test', random.random()), 'tt@tt.com', 'testpassword')
        user.save()
        return user
    
    ''' create and return default subscription for current user '''
    def getSubscription(self, user):
        s = Subscription(owner=user, monthly_fee=0)
        s.save()
        return s
    
    ''' test method Dashboard.total_users() ''' 
    def test_total_users(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.total_users(), 0)
        u = self.getUser()

        self.failUnlessEqual(Dashboard.total_users(), 1)
        u.delete()
        self.failUnlessEqual(Dashboard.total_users(), 0)
        
    ''' test method Dashboard.average_signups() '''
    def test_average_signups(self):
        # Empty database has no signups
        self.failUnlessEqual(Dashboard.average_signups(), '0 / 0 / 0')
        
        u = self.getUser()
        # create subscription for today
        s = self.getSubscription(u)
        self.failUnlessEqual(Dashboard.average_signups(), '1 / 1 / 1')
        
        # change date_created 3 days ago for weekly
        s.date_created -= datetime.timedelta(days=3)  
        s.save()
        self.failUnlessEqual(Dashboard.average_signups(), '0 / 1 / 1')
        
        # change date_created 23 days ago for monthly
        s.date_created -= datetime.timedelta(days=20)  
        s.save()
        self.failUnlessEqual(Dashboard.average_signups(), '0 / 0 / 1')
        
        # Delete all data
        u.delete()        
        self.failUnlessEqual(Dashboard.average_signups(), '0 / 0 / 0')
        
    ''' test method Dashboard.left_daily() '''
    def test_left_daily(self):
        u = self.getUser()
        now = datetime.datetime.now()
        
        # Empty database has no users
        self.failUnlessEqual(Dashboard.left_daily(), 0)
        
        # create 1 user which left today
        s = Subscription(owner=u, monthly_fee=0)        
        s.date_cancelled = now
        s.date_deleted = now
        s.save()
        
        self.failUnlessEqual(Dashboard.left_daily(), 1)
        
        # Delete all data
        u.delete()        
        self.failUnlessEqual(Dashboard.left_monthly(), 0)
        
    ''' test method Dashboard.left_weekly() '''
    def test_left_weekly(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.left_weekly(), 0)
        
        # create 1 user which left 3 days before
        u = self.getUser()
        date = datetime.datetime.now() - datetime.timedelta(days=3)        
        
        s = Subscription(owner=u, monthly_fee=0)        
        s.date_cancelled = date
        s.date_deleted = date
        s.save()
        
        self.failUnlessEqual(Dashboard.left_weekly(), 1)
    
        # Delete all data
        u.delete()  
        self.failUnlessEqual(Dashboard.left_monthly(), 0)
        
    ''' test method Dashboard.left_monthly() '''
    def test_left_monthly(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.left_monthly(), 0)
        
        # create 1 user which left 20 days before
        u = self.getUser()
        date = datetime.datetime.now() - datetime.timedelta(days=20)         
        
        s = Subscription(owner=u, monthly_fee=0)        
        s.date_cancelled = date
        s.date_deleted = date
        s.save()
        
        self.failUnlessEqual(Dashboard.left_monthly(), 1)
    
        # Delete all data
        u.delete()        
        self.failUnlessEqual(Dashboard.left_monthly(), 0)
    
    ''' test method Dashboard.churn_rage_per_time() '''
    def test_churn_rage_per_time(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.churn_rage_per_time(), '0 / 0 / 0')
        
        # create user which left 20 days before 
        u = self.getUser()
        now = datetime.datetime.now()
        date = now - datetime.timedelta(days=20)     
        s = Subscription(owner=u, monthly_fee=0)        
        s.date_cancelled = date
        s.date_deleted = date
        s.save()
        
        self.failUnlessEqual(Dashboard.churn_rage_per_time(), '0 / 0 / 1')
    
        # create user which left 3 days before 
        date = now - datetime.timedelta(days=3)
        s.date_cancelled = date
        s.date_deleted = date
        s.save()
        
        self.failUnlessEqual(Dashboard.churn_rage_per_time(), '0 / 1 / 1')
    
        # create user which left today
        s.date_cancelled = now
        s.date_deleted = now
        s.save()        
        self.failUnlessEqual(Dashboard.churn_rage_per_time(), '1 / 1 / 1')
        
        # Delete all data
        u.delete()
        self.failUnlessEqual(Dashboard.churn_rage_per_time(), '0 / 0 / 0')
    
    ''' test method Dashboard.churn_acquisition() '''
    def test_churn_acquisition(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.churn_acquisition(), '0% / 0% / 0%')
        
        # create user which left today
        date = datetime.datetime.now()
        u = self.getUser()
        s = Subscription(owner=u, monthly_fee=0)        
        s.date_cancelled = date
        s.date_deleted = date
        s.save()
        
        self.failUnlessEqual(Dashboard.churn_acquisition(), '100% / 100% / 100%')

        # create user which left 3 days before
        date -= datetime.timedelta(days=3)     
        s.date_cancelled = date
        s.date_deleted = date
        s.save()        
        self.failUnlessEqual(Dashboard.churn_acquisition(), '0% / 100% / 100%')
        
        # create user which left 23 days before
        date -= datetime.timedelta(days=20)
        s.date_cancelled = date
        s.date_deleted = date
        s.save()        
        self.failUnlessEqual(Dashboard.churn_acquisition(), '0% / 0% / 100%')
        
        # Delete all data
        u.delete()
        self.failUnlessEqual(Dashboard.churn_acquisition(), '0% / 0% / 0%')
        
    ''' test method Dashboard.not_access_users() '''
    def test_not_access_users(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.not_access_users(), '0%(0) / 0%(0)')
        
        now = datetime.datetime.now()
        # create 1 user with last login 3 days before
        u = User.objects.create_user('not_access', 'tt@tt.com', 'testpassword')
        u.last_login = now - datetime.timedelta(days=3)
        u.save()        
        self.failUnlessEqual(Dashboard.not_access_users(), '100%(1) / 100%(1)')
        
        # create second user with last login 20 days before
        u2 = User.objects.create_user('not_access2', 'tt@tt.com', 'testpassword')
        u2.last_login = now - datetime.timedelta(days=20)
        u2.save()        
        self.failUnlessEqual(Dashboard.not_access_users(), '50%(1) / 100%(2)')
        
        # delete second user
        u.delete()
        self.failUnlessEqual(Dashboard.not_access_users(), '0%(0) / 100%(1)')

        #delete all users
        u2.delete()        
        self.failUnlessEqual(Dashboard.not_access_users(), '0%(0) / 0%(0)')
    
    ''' test method Dashboard.not_activate_users() '''
    def test_not_activate_users(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.not_activate_users(), 0)
        
        # create 1 not active user
        u = User.objects.create_user('test', 'tt@tt.com', 'testpassword')
        u.is_active = 0
        u.save()
        self.failUnlessEqual(Dashboard.not_activate_users(), 1)
        
        # Delete all data
        u.delete()
        self.failUnlessEqual(Dashboard.not_activate_users(), 0  )
    
    ''' create file for current subscription '''
    def getFile(self, subscription):
        file = File(date_expires=datetime.datetime.now(), account=subscription)
        file.save()
        return file
    
    ''' test method Dashboard.average_files() '''
    def test_average_files(self):
        # Empty database has no files
        self.failUnlessEqual(Dashboard.average_files(), '0.0')
        
        # create 1 user and 1 file
        u = self.getUser()
        s = self.getSubscription(u)
        f = self.getFile(s)
        self.failUnlessEqual(Dashboard.average_files(), '1.0')
        
        # create second user
        u2 = self.getUser()
        s2 = self.getSubscription(u2)
        self.failUnlessEqual(Dashboard.average_files(), '0.5')
        
        # create file for second user
        f2 = self.getFile(s2)
        self.failUnlessEqual(Dashboard.average_files(), '1.0')
        
        # delete all users
        u.delete()
        u2.delete()
        self.failUnlessEqual(Dashboard.average_files(), '0.0')
    
    ''' create share for current sender '''
    def getShare(self, user):
        share = Share(user_created=user)
        share.save()
        return share
    
    ''' test method Dashboard.average_shares() '''
    def test_average_shares(self):
        # Empty database has no shares
        self.failUnlessEqual(Dashboard.average_shares(), '0.0')
        
        # create 1 share for 1 sender 
        u = self.getUser()
        sh = self.getShare(u)
        self.failUnlessEqual(Dashboard.average_shares(), '1.0')
        
        # create second user
        u2 = self.getUser()
        self.failUnlessEqual(Dashboard.average_shares(), '0.5')
        
        # create share for second user
        sh2 = self.getShare(u2)
        self.failUnlessEqual(Dashboard.average_shares(), '1.0')
        
        # delete all users
        u.delete()
        u2.delete()
        self.failUnlessEqual(Dashboard.average_shares(), '0.0')
    
    def getReceipt(self, subscription, amount):    
        receipt = Receipt(amount=amount, user_created=subscription.owner, monthly_fee=0,
                    tax_rate=0, tax_amount=0, transaction_id=random.random(),
                subtotal=0, total=0, amount_paid=0, subscription_id=subscription.id, plan_id=1)
        receipt.save()
        return receipt
    
    ''' test method Dashboard.average_lifetime_in_months() '''
    def test_average_lifetime_in_months(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.average_lifetime_in_months(), '0.0')
        
        # Create user with date_created = now
        u = self.getUser()
        s = self.getSubscription(u)
        self.failUnlessEqual(Dashboard.average_lifetime_in_months(), '0.0')
        
        # change date_created = -1 month
        s.date_created -= datetime.timedelta(days=30)
        s.save()
        self.failUnlessEqual(Dashboard.average_lifetime_in_months(), '1.0')
        
        # Create user with date_created = -3 months
        u2 = self.getUser()
        s2 = self.getSubscription(u2)
        s2.date_created -= datetime.timedelta(days=90)
        s2.save()
        self.failUnlessEqual(Dashboard.average_lifetime_in_months(), '2.0')

        # delete all data
        u.delete()
        u2.delete()
        self.failUnlessEqual(Dashboard.average_lifetime_in_months(), '0.0')
        
    
    ''' test method Dashboard.average_lifetime_in_dollars() '''
    def test_average_lifetime_in_dollars(self):
        # Empty database has no users
        self.failUnlessEqual(Dashboard.average_lifetime_in_dollars(), '0.00')
        
        # create receipt with amount = 10
        u = self.getUser()
        s = self.getSubscription(u)
        r = self.getReceipt(s, decimal.Decimal(10))        
        self.failUnlessEqual(Dashboard.average_lifetime_in_dollars(), '10.00')
        
        # create receipt with amount = 20
        u2 = self.getUser()
        s2 = self.getSubscription(u2)
        r2 = self.getReceipt(s2, decimal.Decimal(20))        
        self.failUnlessEqual(Dashboard.average_lifetime_in_dollars(), '15.00')
        
        # delete receipt with amount = 10
        r.delete()
        self.failUnlessEqual(Dashboard.average_lifetime_in_dollars(), '20.00')
        
        # remove all data
        r2.delete()
        u.delete()
        u2.delete()
        self.failUnlessEqual(Dashboard.average_lifetime_in_dollars(), '0.00')

    
    ''' test method Dashboard.monthly_revenue() '''
    def test_monthly_revenue(self):
        # Empty database has no receipts
        self.failUnlessEqual(Dashboard.monthly_revenue(), '0.00')
        u = self.getUser()
        s = self.getSubscription(u)
        
        # set amount 10 for 1 receipt
        r = self.getReceipt(s, decimal.Decimal(10))        
        self.failUnlessEqual(Dashboard.monthly_revenue(), '10.00')
        
        # set amount 20 for 1 receipt
        r2 = self.getReceipt(s, decimal.Decimal(20))
        self.failUnlessEqual(Dashboard.monthly_revenue(), '30.00')
        
        # remove receipt with amount=10
        r.delete()
        self.failUnlessEqual(Dashboard.monthly_revenue(), '20.00')
        
        # remove all data
        r2.delete()
        u.delete()
        self.failUnlessEqual(Dashboard.monthly_revenue(), '0.00')      
        
    

