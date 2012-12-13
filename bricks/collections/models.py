import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from bricks.models import Brick


class Collection(Brick):

    class Meta:
        verbose_name = _(u"collection")
        verbose_name_plural = _(u"collections")


class CollectionObject(models.Model):
    collection = models.ForeignKey(
        related_name="collection_objects",
        to=Collection,
        verbose_name=_(u"collection"))
    from_date = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_(u"from date"))
    to_date = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_(u"to date"))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
