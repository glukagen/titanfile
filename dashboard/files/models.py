from django.db import models
from common.models import BaseModel
#from common.signals import set_slug_code
from accounts.models import Subscription, Group

# Create your models here.
class File(BaseModel):
    file = models.FileField(upload_to='uploads/%Y/%m/%d')
    mimetype = models.CharField(max_length=64, editable=False)
    date_expires = models.DateTimeField(blank=True, null=True, default='');
    hits = models.PositiveIntegerField(editable=False, default=0)
    account = models.ForeignKey(Subscription, related_name='files')
    groups = models.ManyToManyField(Group, blank=True)

    def get_user_files_qs(user, active=True):
        '''
        Return a queryset of all active files owned by the user
            - used as a helper function
        '''
        if active:
            file_list = File.objects.active().filter(user_created = user)
        else:
            file_list = File.objects.deleted().filter(user_created = user)
        return file_list.distinct()

    @staticmethod
    def get_groups_files_qs(user, active=True):
        '''
        Return a queryset of all active files owned by the user's groups
            - used as a helper function
        '''
        if active:
            file_list = File.objects.active().filter(groups__in=user.get_profile().groups.active())
        else:
            file_list = File.objects.deleted().filter(groups__in=user.get_profile().groups.active())
        return file_list.distinct()

    @staticmethod
    def get_account_files_qs(user, active=True):
        '''
        Return a queryset of all active files under the account
            - used as a helper function
        '''
        if active:
            file_list = File.objects.active().filter(account=user.get_profile().account)
        else:
            file_list = File.objects.deleted().filter(account=user.get_profile().account)
        return file_list.distinct()

    @staticmethod
    def get_share_files_qs(user):
        '''
        Return a queryset of all active files shared with the user
            - used as a helper function
        '''
        file_list = File.objects.active().filter(share__recipient=user)
        return file_list.distinct()

    @staticmethod
    def get_access_files_qs(user):
        '''
        Return a queryset of all files viewable by a user
        '''
        if user.get_profile().is_account_admin():
            file_list = File.get_account_files_qs(user)
        else:
            file_list = File.get_user_files_qs(user) | File.get_groups_files_qs(user) | File.get_share_files_qs(user)
        return file_list.distinct()

    @staticmethod
    def get_share_files_qs(user):
        '''
        Return a queryset of all files sharable by a user
        '''
        if user.get_profile().is_account_admin():
            file_list = File.get_account_files_qs(user)
        else:
            file_list = File.get_user_files_qs(user) | File.get_groups_files_qs(user)
        return file_list.distinct()

    @staticmethod
    def get_change_files_qs(user):
        '''
        Return a queryset of all files changeable by a user
        '''
        if user.get_profile().is_account_admin():
            file_list = File.get_account_files_qs(user)
        else:
            file_list = File.get_user_files_qs(user)
        return file_list.distinct()

    @staticmethod
    def get_deleted_files_qs(user):
        '''
        Return a queryset of all file in the user's trash
        '''
        if user.get_profile().is_account_admin():
            file_list = File.get_account_files_qs(user, active=False)
        else:
            file_list = File.get_user_files_qs(user, active=False)
        return file_list.distinct()

