from django.contrib import admin
from django.conf import settings
from django import forms

from bricks.admin import PageInlineAdmin
from bricks.collections.admin import CollectionObjectInlineAdmin

from .models import Article, ArticleSection

from bricks import USE_TINYMCE
if USE_TINYMCE:
    from tinymce.widgets import TinyMCE


class ArticleSectionForm(forms.ModelForm):
    if USE_TINYMCE:
        text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)

    class Meta:
        model = ArticleSection


class ArticleSectionInlineAdmin(admin.StackedInline):
    model = ArticleSection
    extra = 0
    form = ArticleSectionForm


class ArticleForm(forms.ModelForm):
    if USE_TINYMCE:
        description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = ArticleSection


class ArticleAdmin(admin.ModelAdmin):
    inlines = [PageInlineAdmin, ArticleSectionInlineAdmin, CollectionObjectInlineAdmin]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('picture', )


admin.site.register(Article, ArticleAdmin)
