import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from .managers import PublicationManager


class PublicationAbstract(models.Model):
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is active'))
    add_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
        verbose_name=_('creation date'))
    mod_date = models.DateTimeField(
        auto_now=True,
        blank=True,
        editable=False,
        null=True,
        verbose_name=_("last modification date"))
    pub_date = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_("publication date"),
        help_text=_("For an entry to be published, it must be active and its "
                    "publication date must be in the past."))
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("publication end date"))

    objects = PublicationManager()

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'


class SiteAbstract(models.Model):
    sites = models.ManyToManyField('sites.Site')
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class MPTTAbstract(MPTTModel):
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('parent'))

    class Meta:
        abstract = True


class Tie(MPTTAbstract, PublicationAbstract, SiteAbstract):
    title = models.CharField(
        verbose_name=_(u"title"))
    slug = models.SlugField(
        verbose_name=_(u"slug"))
    description = models.CharField(
        blank=True,
        null=True,
        verbose_name=_(u"description"))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta(MPTTAbstract.Meta, PublicationAbstract.Meta, SiteAbstract.Meta):
        verbose_name = _(u"tie")
        verbose_name_plural = _(u"ties")

    def __unicode__(self):
        return self.title


class TiedObject(models.Model):
    ties = generic.GenericRelation(
        to=Tie,
        content_type_field='content_type',
        object_id_field='object_pk')
