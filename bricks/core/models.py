'''
Created on 21-09-2011

@author: Rafał Selewońko <rafal@selewonko.com>
'''
from bricks.core.managers import BrickManager, CurrentSiteBrickManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


class BaseAbstract(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'),
        auto_now_add=True, editable=False, null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True,
        verbose_name=_("publication end date"), null=True, blank=True)
    user = models.ForeignKey('auth.User', editable=False,
        verbose_name=_('user'), blank=True, null=True)

    class Meta:     # IGNORE:W0232
        abstract = True


class BrickAbstract(BaseAbstract):
    is_active = models.BooleanField(verbose_name=_('is active'),
        default=False, help_text=_("Tick to make this entry live (see also the"
            " publication date). Note that administrators (like yourself) are "
            "allowed to preview inactive entries whereas the general public "
            "aren't."))
    pub_date = models.DateTimeField(default=datetime.now,
        verbose_name=_("publication date"), null=True, blank=True,
        help_text=_("For an entry to be published, it must be active and its "
            "publication date must be in the past."))
    end_date = models.DateTimeField(verbose_name=_("publication end date"),
        null=True, blank=True)
    sites = models.ManyToManyField('sites.Site')

    objects = BrickManager()
    on_site = CurrentSiteBrickManager()

    class Meta:     # IGNORE:W0232
        abstract = True
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
