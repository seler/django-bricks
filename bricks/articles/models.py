from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from bricks.models import Brick


ARTICLE_SECTION_TYPE_TEMPLATE_NAME_CHOICES = \
    getattr(settings, 'BRICK_ARTICLE_SECTION_TYPE_TEMPLATE_NAME_CHOICES', None)
ARTICLE_TEMPLATE_NAME_CHOICES = \
    getattr(settings, 'BRICK_ARTICLE_TEMPLATE_NAME_CHOICES', None)
ARTICLE_SECTION_TYPES = \
    getattr(settings, 'BRICKS_ARTICLE_SECTION_TYPES', dict())
ARTICLE_SECTION_TYPE_CHOICES = \
    tuple([(key, value['name']) for key, value in ARTICLE_SECTION_TYPES.items()])
ARTICLE_SECTION_TYPE_DEFAULT = \
    getattr(settings, 'BRICKS_ARTICLE_SECTION_TYPE_DEFAULT', None)


class Article(Brick):

    template_name = models.CharField(
        blank=True,
        null=True,
        choices=ARTICLE_TEMPLATE_NAME_CHOICES,
        max_length=64,
        verbose_name=_(u"template name"))

    class Meta:
        verbose_name = _(u"article")
        verbose_name_plural = _(u"articles")
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

        return [relations[item.content_type_id][item.object_id] for item in collection_objects]

    def get_absolute_url(self):
        return super(Article, self).get_absolute_url()


class ArticleSection(models.Model):
    article = models.ForeignKey(
        related_name="article_sections",
        to=Article,
        verbose_name=_(u"article"))
    article_section_type = models.PositiveIntegerField(
        choices=ARTICLE_SECTION_TYPE_CHOICES,
        default=ARTICLE_SECTION_TYPE_DEFAULT,
        verbose_name=_(u"article section type"))
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"object id"))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_(u"order"))
    text = models.TextField(
        blank=True,
        verbose_name=_(u"text"))

    class Meta:
        verbose_name = _(u"article section")
        verbose_name_plural = _(u"articles section")
