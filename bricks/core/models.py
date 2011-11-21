import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from bricks.core.managers import BaseManager, CurrentSiteBaseManager


class BaseAbstract(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('creation date'))
    modification_date = models.DateTimeField(auto_now=True, blank=True, editable=False, null=True, verbose_name=_("last modification date"))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=_("publication date"),
                                    help_text=_("For an entry to be published, it must be active and its "
                                                "publication date must be in the past."))
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=_("publication end date"))

    sites = models.ManyToManyField('sites.Site')

    objects = BaseManager()
    on_site = CurrentSiteBaseManager()

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'


class MPTTBaseAbstract(MPTTModel, BaseAbstract):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_('parent'))
