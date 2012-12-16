import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from bricks.models import Brick
from .managers import CollectionObjectManager


class Collection(Brick):

    template_name = models.CharField(
        blank=True,
        null=True,
        max_length=64,
        verbose_name=_(u"template name"))

    class Meta:
        verbose_name = _(u"collection")
        verbose_name_plural = _(u"collections")

    def get_objects(self):
        queryset = self.collection_objects.published()

        generics = {}
        for item in queryset:
            generics.setdefault(item.content_type_id, set()).add(item.object_id)

        content_types = ContentType.objects.in_bulk(generics.keys())

        relations = {}
        for ct, fk_list in generics.items():
            ct_model = content_types[ct].model_class()
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))

        for item in queryset:
            yield relations[item.content_type_id][item.object_id]

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

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CollectionObjectManager()
