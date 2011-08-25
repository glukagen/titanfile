from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from common.models import BaseModel
#from common.signals import set_slug_code
from accounts.countries import COUNTRIES, COUNTRIES_DICT
from accounts.provinces import STATE_PROVINCE, STATE_PROVINCE_DICT
from accounts.industries import INDUSTRIES, INDUSTRIES_DICT
#from shares.models import Share
from django.contrib.localflavor.us.models import PhoneNumberField


class Receipt(models.Model):
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    user_created = models.ForeignKey(User, default=1, related_name='%(class)s_user_created')
    date_created = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, default=1, related_name='%(class)s_user_modified')
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100)
    subscription_id = models.IntegerField()
    plan_id = models.IntegerField()    
    monthly_fee = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    month = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    tax_rate = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    #currency = support_type = models.CharField(max_length=3, default='CAD')
    billing_option = models.CharField(max_length=2, default='PA')    
    cc_last_four_digit = models.CharField(max_length=100)
    cc_first_name = models.CharField(max_length=30)
    cc_last_name = models.CharField(max_length=30)

SUPPORT_TYPES = (
    ('0', 'Community'),
    ('1', 'Email'),
    ('2', 'Phone'),
    ('3', 'Phone 24/7'),
)

SUPPORT_TYPES_DICT = {
    '0': 'Community',
    '1': 'Email',
    '2': 'Phone',
    '3': 'Phone 24/7',
}

PLAN_STATUS_TYPES = (
    ('A', 'Active'),    # People can sign up with this plan
    ('I', 'Inactive'),  # No new signups, may have some existing users
    ('D', 'Deleted'),    # No one has access to this plan
)

PLAN_STATUS_TYPES_DICT = {
    'A': 'Active',
    'I': 'Inactive',
    'D': 'Deleted',
}

SUBSCRIPTION_STATUS_TYPES = (
    ('A', 'Active'),    # in good standing
    ('C', 'Cancelled'), # Cancellation requested, but not expired
    ('D', 'Deleted'),   # The user has request complete obleteration of this account
)

SUBSCRIPTION_STATUS_TYPES_DICT = {
    'A': 'Active',
    'C': 'Cancelled',
    'D': 'Deleted',
}

CC_TYPES = (
    ('V', 'Visa'),
    ('M', 'MasterCard'),
    ('P', 'PayPal'),
    ('O', 'Other'),
)

CC_TYPES_DICT = {
    'M': 'MasterCard',
    'O': 'Other',
    'P': 'PayPal',
    'V': 'Visa',
}

class Plan(BaseModel):
    ''' Define different plans. A plan should never be modified, only new plans added with revised parameters.
        - Max value of 0 = feature is disabled
        - Max value of -1 = unlimited
    '''
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=PLAN_STATUS_TYPES, default='A')

    date_activated = models.DateTimeField(blank=True, null=True, default=None)
    date_inactivated = models.DateTimeField(blank=True, null=True, default=None)
    date_deleted = models.DateTimeField(blank=True, null=True, default=None)

    max_users = models.IntegerField(default=-1)
    max_files = models.IntegerField(default=-1)
    max_shares = models.IntegerField(default=-1)
    #max_bytes = models.IntegerField(default=-1)
    max_file_size = models.IntegerField(default=-1)
    branding = models.BooleanField(default=False)
    #domain = models.BooleanField(default=False)
    #subdomain = models.BooleanField(default=False)
    encryption = models.BooleanField(default=True)
    #recipient_verification = models.BooleanField(default=True)
    support_type = models.CharField(max_length=1, choices=SUPPORT_TYPES, default='0')

    #setup_fee = models.IntegerField(default=0, blank=True, null=True)
    monthly_fee = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    trial_period = models.IntegerField(default=30) # 30 days by default

    notes = models.TextField(blank=True, null=True)
  
    
class Subscription(BaseModel):
    MONTH_TYPES = [(x, x) for x in xrange(1, 13)]
    YEAR_TYPES = [(x, x) for x in xrange(date.today().year, date.today().year + 15)]

    status = models.CharField(max_length=1, choices=SUBSCRIPTION_STATUS_TYPES, default='A')
    date_expires = models.DateTimeField(blank=True, null=True, default=None)
    date_cancelled = models.DateTimeField(blank=True, null=True, default=None)
    date_deleted = models.DateTimeField(blank=True, null=True, default=None)

    plan = models.ForeignKey(Plan, default=1)
    
    owner = models.ForeignKey(User, unique=True)
    referral = models.CharField(max_length=64, blank=True, null=True, default=None)
    domain = models.CharField(max_length=128, blank=True, null=True, default=None)
    subdomain = models.CharField(max_length=128, blank=True, null=True, default=None, unique=True)

    # Billing Info
    company_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    industry = models.CharField(choices=INDUSTRIES, max_length=2, blank=True, null=True, default=None)
    address1 = models.CharField(max_length=64, blank=True, null=True, default=None)
    address2 = models.CharField(max_length=64, blank=True, null=True, default=None)
    city = models.CharField(max_length=64, blank=True, null=True, default=None)
    province = models.CharField(choices=STATE_PROVINCE, max_length=2, blank=True, null=True, default=None)
    country = models.CharField(max_length=64, blank=True, null=True, default=None)
    country_code = models.CharField(max_length=2, blank=True, null=True, default=None, choices=COUNTRIES, verbose_name='Country')
    postal_code = models.CharField(max_length=10, blank=True, null=True, default=None)
    phone = PhoneNumberField(blank=True, null=True)
    cell = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)

    max_users = models.IntegerField(default=-1)
    max_files = models.IntegerField(default=-1)
    max_shares = models.IntegerField(default=-1)
    #max_bytes = models.IntegerField(default=-1)
    max_file_size = models.IntegerField(default=-1)
    branding = models.BooleanField(default=False)
    #domain = models.BooleanField(default=False)
    #subdomain = models.BooleanField(default=False)
    encryption = models.BooleanField(default=True)
    #recipient_verification = models.BooleanField(default=True)
    support_type = models.CharField(max_length=1, choices=SUPPORT_TYPES, default='0')

    #setup_fee = models.IntegerField(default=0, blank=True, null=True)
    monthly_fee = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    trial_period = models.IntegerField(default=30) # 30 days by default
    code = models.CharField(max_length=30, blank=True, null=True)

    cc_first_name = models.CharField(max_length=30, null=True, blank=True, default=None)
    cc_last_name = models.CharField(max_length=30, null=True, blank=True, default=None)
    cc_type = models.CharField(choices=CC_TYPES, max_length=1, default='O')
    cc_number = models.CharField(max_length=20, blank=True, null=True, default=None)
    #cc_month = models.CharField(max_length=2, choices=MONTH_TYPES, blank=True, null=True) 
    #cc_year = models.CharField(max_length=4, choices=MONTH_TYPES, blank=True, null=True) 
    cc_month = models.IntegerField(max_length=2, blank=True, null=True, default=0)
    cc_year = models.IntegerField(max_length=4, blank=True, null=True, default=0)

    notes = models.TextField(blank=True, null=True)
        

class Group(BaseModel):
    description = models.TextField(blank=True)
    account = models.ForeignKey(Subscription)
    
    class Meta:
        unique_together = ('account', 'name')

class UserProfile(BaseModel):
    url = models.URLField(blank=True, null=True)
    #home_address = models.TextField()
    #phone_numer = models.PhoneNumberField()
    user = models.ForeignKey(User, unique=True)
    account = models.ForeignKey(Subscription, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)

def user_post_save(sender, instance, signal, *args, **kwargs):
    profile, new = UserProfile.objects.get_or_create(user=instance)
    profile.name = instance.username
    profile.save()
    if False:
        profile.account = Subscription.objects.create(
            name = instance.get_full_name(),
            type=settings.ACCOUNT_TYPE_FREE,
            owner=instance
        )
        profile.save()

models.signals.post_save.connect(user_post_save, sender=User)
