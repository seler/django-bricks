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

    @property
    def sections(self):
        try:
            return self._sections
        except AttributeError:
            self._sections = self.get_sections()
            return self._sections

    def get_sections(self):
        article_sections = list(self.article_sections.all())
        from django.db.models.loading import get_model

        generics = {}
        for item in article_sections:
            if item.object_id:
                generics.setdefault(item.article_section_type, list()).append(item.object_id)

        relations = {}
        for article_section_type, fk_list in generics.items():
            section_type = ARTICLE_SECTION_TYPES[article_section_type]
            model_class = get_model(section_type['app_label'], section_type['model_name'])
            relations[article_section_type] = model_class.objects.in_bulk(list(fk_list))

        sections = []
        for item in article_sections:
            section = ARTICLE_SECTION_TYPES[item.article_section_type]
            if item.object_id:
                section['object'] = relations[item.article_section_type][item.object_id]
            section['text'] = item.text
            sections.append(section)
        return sections

    def get_absolute_url(self):
        return super(Article, self).get_absolute_url()


class ArticleSection(models.Model):
    article = models.ForeignKey(
        related_name="article_sections",
        to=Article,
        verbose_name=_(u"article"))
    article_section_type = models.CharField(
        choices=ARTICLE_SECTION_TYPE_CHOICES,
        default=ARTICLE_SECTION_TYPE_DEFAULT,
        max_length=32,
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
        ordering = ['order', 'id']
