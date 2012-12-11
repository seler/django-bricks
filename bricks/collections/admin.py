from django.contrib import admin

from bricks.admin import TieInlineAdmin
from .models import Collection


class CollectionAdmin(admin.ModelAdmin):
    inlines = [TieInlineAdmin]


admin.site.register(Collection, CollectionAdmin)
