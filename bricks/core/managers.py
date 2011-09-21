# -*- coding: utf-8 -*-
'''
Created on 21-09-2011

@author: Rafał Selewońko <rafal@selewonko.com>
'''

from django.db import models
from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager

Q = models.Q
NOW = datetime.now()


class BrickManager(models.Manager):
    '''Be sure to always use ``published`` in your views, templated tags, etc.
    Use ``CurrentSiteBaseManager`` to retrieve object on current site.'''

    def published(self):
        return super(BrickManager, self).get_query_set().filter(
                        Q(is_active=True),
                        Q(pub_date__lte=NOW),
                        Q(end_date__gt=NOW) | Q(end_date__isnull=True),
                    )
    active = published


class CurrentSiteBrickManager(BrickManager, CurrentSiteManager):
    pass
