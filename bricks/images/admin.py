from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from bricks.admin import TieInlineAdmin

from .models import Image, ResizedImage
from .image import crop_image, get_image


class ImageAdmin(admin.ModelAdmin):
    inlines = [TieInlineAdmin]
    list_display = ['thumbnail', 'basename']

    def thumbnail(self, obj):
        if obj.image:
            html = """<div style="width: 320px; text-align: center;"><img src="{0}" /></div>"""
            return html.format(get_image(obj.image, ResizedImage.MODE_SCALE, 320, 180))
        else:
            return "no-image"
    thumbnail.allow_tags = True
    thumbnail.short_description = u'thumbnail'


class CroppedListFilter(SimpleListFilter):
    title = _('cropped')
    parameter_name = 'cropped'
    VAL_CROPPED = '1'
    VAL_NOTCROPPED = '0'

    def lookups(self, request, model_admin):
        return (
            (self.VAL_CROPPED, _('Cropped')),
            (self.VAL_NOTCROPPED, _('Not cropped')),
        )

    def queryset(self, request, queryset):
        val = None
        if self.value() == self.VAL_CROPPED:
            val = False
        if self.value() == self.VAL_NOTCROPPED:
            val = True
        if val is not None:
            return queryset.filter(crop_x1__isnull=val, crop_y1__isnull=val, crop_x2__isnull=val, crop_y2__isnull=val)


class ResizedImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'original_name', 'width', 'height', 'mode', 'cropped']
    readonly_fields = ['original_name', 'resized_name', 'width', 'height', 'mode', 'error']
    list_filter = ['mode', CroppedListFilter, 'error']

    def thumbnail(self, obj):
        if obj.resized_name.name:
            html = """<div style="width: 320px; text-align: center;">
            <img src="{0}" style="max-width: 320px; max-height: 180px;" /></div>"""
            return html.format(obj.resized_name.url, obj.width, obj.height)
        else:
            return "no-image"
    thumbnail.allow_tags = True
    thumbnail.short_description = u'thumbnail'

    def save_model(self, request, obj, form, change):
        if obj.cropped():
            obj.resized_name = crop_image(obj.original_name, obj.width, obj.height, obj.crop_x1, obj.crop_y1, obj.crop_x2, obj.crop_y2)
        obj.save()


admin.site.register(Image, ImageAdmin)
admin.site.register(ResizedImage, ResizedImageAdmin)
