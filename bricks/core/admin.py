from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline, BaseGenericInlineFormSet

from .models import Tie


class TieAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super(TieAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.level:
            return False
        return super(TieAdmin, self).has_add_permission(request)


class RequiredInlineFormSet(BaseGenericInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class TieInlineAdmin(GenericStackedInline):
    model = Tie
    extra = 1
    max_num = 1
    formset = RequiredInlineFormSet
    template = "admin/edit_inline/tie_stacked.html"


admin.site.register(Tie, TieAdmin)
