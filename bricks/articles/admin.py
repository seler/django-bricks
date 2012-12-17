from django.contrib import admin

from bricks.admin import PageInlineAdmin
from bricks.collections.admin import CollectionObjectInlineAdmin

from .models import Article, ArticleSection, ArticleSectionType


class ArticleSectionTypeAdmin(admin.ModelAdmin):
    pass


class ArticleSectionInlineAdmin(admin.StackedInline):
    model = ArticleSection
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [PageInlineAdmin, ArticleSectionInlineAdmin, CollectionObjectInlineAdmin]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleSectionType, ArticleSectionTypeAdmin)
