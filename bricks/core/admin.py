from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline, BaseGenericInlineFormSet

from .models import Tie


class TieAdmin(admin.ModelAdmin):
    pass


def TieInlineAdmin(empty_permitted=False):
    class RequiredInlineFormSet(BaseGenericInlineFormSet):
        def _construct_form(self, i, **kwargs):
            form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
            form.empty_permitted = empty_permitted
            return form

    class _TieInlineAdmin(GenericStackedInline):
        model = Tie
        extra = 1
        max_num = 1
        formset = RequiredInlineFormSet
        template = "admin/edit_inline/tie_stacked.html"

    return _TieInlineAdmin

admin.site.register(Tie, TieAdmin)
