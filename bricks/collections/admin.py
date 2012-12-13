from django.contrib import admin

from bricks.admin import PageInlineAdmin
from .models import Collection


class CollectionAdmin(admin.ModelAdmin):
    inlines = [PageInlineAdmin]


admin.site.register(Collection, CollectionAdmin)
