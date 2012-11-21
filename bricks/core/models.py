import datetime

from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from ..utils import inheritors
from .managers import PublicationManager

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('template_name_field',)


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


class SiteAbstract(models.Model):
    sites = models.ManyToManyField('sites.Site')
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class TiedObject(models.Model):
    ties = generic.GenericRelation('Tie')

    def get_tie(self):
        try:
            return self._tie
        except AttributeError:
            self._tie = self.ties.get()
            return self._tie

    def set_tie(self, tie):
        self._tie = tie
        #TODO: ustawiac relacje generyczna

    def del_tie(self, tie):
        del self._tie

    tie = property(get_tie, set_tie, del_tie)

    def get_absolute_url(self):
        return self.tie.get_absolute_url()

    def get_template_names(self, path):
        names = []
        if self._meta.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if name:
                names.append(name)
        else:
            tail = "%s_%s_detail.html" % (
                self._meta.app_label,
                self._meta.object_name.lower(),
            )
            path_elements = path.split('/')
            for i, slug in enumerate(path_elements):
                p = '/'.join(path_elements[:len(path_elements) - i])
                names.append("bricks/ties/%s/%s" % (p, tail,))
            names.append("bricks/ties/%s" % (tail,))
            for i, slug in enumerate(path_elements):
                p = '/'.join(path_elements[:len(path_elements) - i])
                names.append("bricks/ties/%s/tie_detail.html" % (p,))
            names.append("bricks/ties/tie_detail.html")

        return names

    class Meta:
        abstract = True
        template_name_field = None


def tie_content_type_choices_limit():
    def _wrapped():
        models = inheritors(TiedObject)
        return [c.pk for m, c in ContentType.objects.get_for_models(*models).items()]
    return {'id__in': _wrapped}


def tie_default_parent():
    def _wrapped():
        try:
            return Tie.objects.get(level=0)
        except Tie.DoesNotExist:
            return None
    return _wrapped


class Tie(MPTTModel, PublicationAbstract, SiteAbstract):
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

    parent = TreeForeignKey(
        to='self',
        null=True,
        related_name='children',
        verbose_name=_('parent'))

    content_type = models.ForeignKey(
        to=ContentType,
        blank=True,
        null=True,
        limit_choices_to=tie_content_type_choices_limit())
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta(PublicationAbstract.Meta, SiteAbstract.Meta):
        verbose_name = _(u"tie")
        verbose_name_plural = _(u"ties")
        unique_together = (('content_type', 'object_id'), ('slug', 'level'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.parent and self.__class__.objects.filter(level=0).exists() and self.__class__.objects.filter(level=0).get().pk != self.pk:
            raise IntegrityError(u"Only one root node allowed!")
        return super(Tie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        path = '/'
        for p in self.get_ancestors(include_self=True, ascending=False)[1:]:
            path += p.slug + '/'
        return path
