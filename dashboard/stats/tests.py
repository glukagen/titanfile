from django.contrib.auth.models import User
from models import Dashboard
import unittest


''' Test stats Dashboard class methods'''
class DashboardTest(unittest.TestCase):
    
    def test_total_users(self):
        count = User.objects.count()
        self.failUnlessEqual(Dashboard.total_users(), count)
        User.objects.create_user('testname', 'tt@tt.com', 'testpassword').save()
        self.failUnlessEqual(Dashboard.total_users(), count + 1)
        
    def test_average_signups(self):
        self.failUnlessEqual(Dashboard.average_signups(), '0 / 0 / 0')
    
    def test_left_daily(self):
        pass
    
    def test_left_weekly(self):
        pass
    
    def test_left_monthly(self):
        pass
    
    def test_churn_rage_per_time(self):
        pass
    
    def test_churn_acquisition(self):
        pass
    
    def test_not_access_users(self):
        pass
    
    def test_not_activate_users(self):
        pass
    
    def test_average_files(self):
        pass
    
    def test_average_shares(self):
        pass
    
    def test_average_lifetime_in_months(self):
        pass
    
    def test_average_lifetime_in_dollars(self):
        pass
    
    def test_monthly_revenue(self):
        pass
    

''' Test stats Country class methods'''
class CountryTest(unittest.TestCase):
    def test_user_count(self):
        pass
        
        
    

