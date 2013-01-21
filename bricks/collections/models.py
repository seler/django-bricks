import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from bricks.models import Brick
from .managers import CollectionObjectManager


COLLECTIONS_TEMPLATE_NAME_CHOICES = getattr(settings, 'BRICK_COLLECTIONS_TEMPLATE_NAME_CHOICES', None)


class Collection(Brick):

    template_name = models.CharField(
        blank=True,
        null=True,
        choices=COLLECTIONS_TEMPLATE_NAME_CHOICES,
        max_length=64,
        verbose_name=_(u"template name"))

    ORDER_BY_DATE_ASC = 'from_date'
    ORDER_BY_DATE_DESC = '-from_date'
    ORDER_BY_ORDER_ASC = 'order'
    ORDER_BY_ORDER_DESC = '-order'
    ORDER_BY_CHOICES = (
        (ORDER_BY_DATE_ASC, _("date, ascending")),
        (ORDER_BY_DATE_DESC, _("date, descending")),
        (ORDER_BY_ORDER_ASC, _("order, ascending")),
        (ORDER_BY_ORDER_DESC, _("order, descending")),
    )

    order_by = models.CharField(
        choices=ORDER_BY_CHOICES,
        max_length=32,
        verbose_name=_(u"order by"))

    class Meta:
        verbose_name = _(u"collection")
        verbose_name_plural = _(u"collections")
        template_name_field = "template_name"

    def get_objects(self):
        collection_objects = list(self.collection_objects.published().order_by(self.order_by))

        generics = {}
        for item in collection_objects:
            generics.setdefault(item.content_type_id, list()).append(item.object_id)

        content_types = ContentType.objects.in_bulk(generics.keys())

        relations = {}
        for ct, fk_list in generics.items():
            ct_model = content_types[ct].model_class()
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))

        return [relations[item.content_type_id][item.object_id] for item in collection_objects if item.object_id in relations[item.content_type_id]]

    def get_absolute_url(self):
        return super(Collection, self).get_absolute_url()


class CollectionObject(models.Model):
    collection = models.ForeignKey(
        related_name="collection_objects",
        to=Collection,
        verbose_name=_(u"collection"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_(u"is active"))
    from_date = models.DateTimeField(
        default=datetime.datetime.now,
        blank=True,
        null=True,
        verbose_name=_(u"from date"))
    to_date = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_(u"to date"))
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_(u"order"))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CollectionObjectManager()

    def __unicode__(self):
        try:
            return self.content_object.__unicode__()
        except AttributeError:
            return "{0} {1}".format(self.content_type.name, self.object_id)
