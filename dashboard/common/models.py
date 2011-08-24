from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site

class BaseModelManager(models.Manager):
    #def all(self):
    #    return super(BaseModelManager,self).all()

    def active(self):
        return super(BaseModelManager,self).all().filter(is_active=True, user_created__is_active=True)

    def deleted(self):
        return super(BaseModelManager,self).all().filter(is_active=False, user_created__is_active=True)

    def get_query_set(self):
        qs = super(BaseModelManager, self).get_query_set()
        qs.delete = BaseModelManager._delete_query_set
        #return qs.filter(is_active=True, user_created__is_active=True)
        return qs

    def force_all(self):
        return super(BaseModelManager,self).all()

    @staticmethod
    def _delete_query_set(self):
        for item in self:
            item.delete()

class BaseModel(models.Model):
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    #site = models.ForeignKey(Site, default=0)
    #site = models.ForeignKey(Site, default=Site.objects.get_current, related_name='%(class)s_site')
    user_created = models.ForeignKey(User, default=1, related_name='%(class)s_user_created')
    #date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, default=1, related_name='%(class)s_user_modified')
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True

