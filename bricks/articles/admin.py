from django.contrib import admin

from bricks.admin import PageInlineAdmin
from bricks.collections.admin import CollectionObjectInlineAdmin

from .models import Article, ArticleSection


class ArticleSectionInlineAdmin(admin.StackedInline):
    model = ArticleSection
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [PageInlineAdmin, ArticleSectionInlineAdmin, CollectionObjectInlineAdmin]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('picture', )


admin.site.register(Article, ArticleAdmin)
