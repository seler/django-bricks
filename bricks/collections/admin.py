from django.contrib import admin

from ..core.admin import TieInlineAdmin
from .models import Collection


class CollectionAdmin(admin.ModelAdmin):
    inlines = [TieInlineAdmin]


admin.site.register(Collection, CollectionAdmin)
