from django.db import models
from common.models import BaseModel
from files.models import File
from django.contrib.auth.models import User
from accounts.models import Group
from django.contrib.localflavor.us.models import PhoneNumberField
#from common.signals import set_slug_code

class ExternalUser(BaseModel):
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)
    
class Share(BaseModel):
    """ Each combination of file with recipient, group, or account is a single share. """
    sender = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_sender')
    recipient = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_recipient')
    to_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    date_expires = models.DateTimeField(blank=True, null=True)
    hits = models.IntegerField(default=0)
    files = models.ManyToManyField(File)
    groups = models.ManyToManyField(Group, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    cc_myself = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    verify_phone = PhoneNumberField(null=True, blank=True)
    verify_pin = models.IntegerField(default=0)
