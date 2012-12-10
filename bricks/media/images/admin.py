from django.contrib import admin

from bricks.core.admin import TieInlineAdmin

from .models import Image, ResizedImage
from .image import crop_image


class ImageAdmin(admin.ModelAdmin):
    inlines = [TieInlineAdmin]


class ResizedImageAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'width', 'height', 'mode', 'cropped']
    readonly_fields = ['original_name', 'resized_name', 'width', 'height', 'mode', 'error']

    def save_model(self, request, obj, form, change):
        if obj.cropped():
            obj.resized_name = crop_image(obj.original_name, obj.width, obj.height, obj.crop_x1, obj.crop_y1, obj.crop_x2, obj.crop_y2)
        obj.save()


admin.site.register(Image, ImageAdmin)
admin.site.register(ResizedImage, ResizedImageAdmin)
