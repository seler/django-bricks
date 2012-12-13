from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline, BaseGenericInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict

from .models import Page


class ModelAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        u"""
        Zwraca podmieniona funkcje akcji, ktora przy wykonaniu loguje
        do standardowej historii Django jej wykonanie.

        `Wyjasnienie jak to dziala <http://youtu.be/x0yQg8kHVcI>`_.
        """

        def wrap(old_func, name, desc):
            def func(admin_instance, request, queryset):
                ret = old_func(admin_instance, request, queryset)
                change_message = _(u"Changelist action: {description}.")
                change_message = change_message.format(description=desc)
                log_this = lambda obj: self.log_change(
                    request, obj, change_message)
                map(log_this, queryset)
                return ret
            return func, name, desc

        old_actions = super(ModelAdmin, self).get_actions(request)

        actions = SortedDict(
            [(key, wrap(*value)) for key, value in old_actions.items()]
        )

        return actions


class PageAdmin(ModelAdmin):

    def get_actions(self, request):
        actions = super(PageAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class RequiredGenericInlineFormSet(BaseGenericInlineFormSet):
    required = True

    def _construct_form(self, i, **kwargs):
        form = super(RequiredGenericInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = not self.required
        return form


class PageInlineAdmin(GenericStackedInline):
    model = Page
    max_num = 1
    extra = 0
    template = "admin/edit_inline/tie_stacked.html"


class RequiredPageInlineAdmin(PageInlineAdmin):
    formset = RequiredGenericInlineFormSet
    extra = 1


admin.site.register(Page, PageAdmin)
