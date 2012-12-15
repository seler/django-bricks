import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from mptt.models import MPTTModel, TreeForeignKey

from bricks.utils import inheritors
from bricks.managers import PublicationManager

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('template_name_field', 'template_name_suffix')


class PublicationAbstract(models.Model):
    is_active = models.BooleanField(
        default=True,
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
        help_text=_("For an entry to be published, it must be active and its publication date must be in the past."))
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("publication end date"))

    objects = PublicationManager()

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'


class Page(MPTTModel, PublicationAbstract):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    title = models.CharField(
        max_length=256,
        verbose_name=_(u"title"))

    slug = models.SlugField(
        verbose_name=_(u"slug"))

    description = models.CharField(
        blank=True,
        max_length=1024,
        null=True,
        verbose_name=_(u"description"))

    content_type = models.ForeignKey(
        to=ContentType,
        blank=True,
        null=True,
        #limit_choices_to=tie_content_type_choices_limit()
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):



TEMPLATE_NAME_FIELD = None
TEMPLATE_NAME_SUFFIX = '_detail'


class Brick(PublicationAbstract):
    title = models.CharField(
        max_length=256,
        verbose_name=_(u"title"))

    slug = models.SlugField(
        verbose_name=_(u"slug"))

    description = models.CharField(
        blank=True,
        max_length=1024,
        null=True,
        verbose_name=_(u"description"))

    picture = models.ForeignKey(
        to='images.Image',
        blank=True,
        null=True,
        verbose_name=_(u"picture"))

    class Meta(PublicationAbstract.Meta):
        verbose_name = _(u"tie")
        verbose_name_plural = _(u"ties")
        template_name_field = TEMPLATE_NAME_FIELD

    def __unicode__(self):
        return self.title

    def get_template_names(self, path):
        names = []
        template_name_suffix = getattr(self._meta, 'template_name_suffix', TEMPLATE_NAME_SUFFIX)
        template_name_field = getattr(self._meta, 'template_name_field', TEMPLATE_NAME_FIELD)
        if template_name_field:
            name = getattr(self.object, template_name_field, None)
            if name:
                names.append(name)
        else:
            template_name = "%s/%s%s.html" % (
                self._meta.app_label,
                self._meta.object_name.lower(),
                template_name_suffix,
            )
            names.append(template_name)
            names.append("bricks/brick/brick_detail.html")

        return names
        template_name_suffix = TEMPLATE_NAME_SUFFIX

    def get_absolute_url(self):
        classes = [self.__class__] + list(inheritors(self.__class__))
        content_types = ContentType.objects.get_for_models(*classes)
        for ct in content_types:
            try:
                page = Page.objects.get(content_type=ct, object_id=self.id)
            except Page.DoesNotExist:
                continue
            else:
                return page.get_absolute_url()
        else:
            return ""


"""
def tie_content_type_choices_limit():
    def _wrapped():
        models = inheritors(TiedObject)
        return [c.pk for m, c in ContentType.objects.get_for_models(*models).items()]
    return {'id__in': _wrapped}
"""


def get_brick(instance):
    if not hasattr(instance, '_brick'):
        models = inheritors(instance.__class__)
        for model in models:
            try:
                instance._brick = getattr(instance, model.__name__.lower())
            except ObjectDoesNotExist:
                continue
            else:
                break
    return instance._brick
