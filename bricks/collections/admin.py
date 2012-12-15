from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline

from bricks.admin import PageInlineAdmin
from .models import Collection, CollectionObject


class LocalCollectionObjectInlineAdmin(admin.TabularInline):
    model = CollectionObject
    extra = 0


class CollectionObjectInlineAdmin(GenericTabularInline):
    model = CollectionObject
    extra = 0


class CollectionAdmin(admin.ModelAdmin):
    inlines = [PageInlineAdmin, CollectionObjectInlineAdmin, LocalCollectionObjectInlineAdmin]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Collection, CollectionAdmin)
