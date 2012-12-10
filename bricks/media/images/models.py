import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from bricks.core.models import TiedObject

from .fields import CropImageField


class Image(TiedObject):
    image = CropImageField(
        upload_to='image/original',
        max_length=256,
        height_field='height',
        width_field='width',
        size_field='size',
        verbose_name=_("image file"))
    width = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_(u"width"))
    height = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_(u"height"))
    size = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_(u"size"))
    meta = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(u"meta"))

    class Meta:
        verbose_name = _(u'image')
        verbose_name_plural = _(u'images')

    def __unicode__(self):
        return self.basename()

    def basename(self):
        return os.path.basename(self.image.name)


def fake_upload_to(*args, **kwargs):
    return ''


class ResizedImage(models.Model):
    MODE_ZOOM = 'zoom'
    MODE_SCALE = 'scale'
    MODE_STRETCH = 'stretch'
    MODE_CHOICES = (
        (MODE_ZOOM, _("Zoom")),
        (MODE_SCALE, _("Scale")),
        (MODE_STRETCH, _("Stretch")),
    )
    original_name = models.ImageField(
        upload_to=fake_upload_to,
        max_length=255,
        editable=False,
        verbose_name=_(u"original"))
    resized_name = models.ImageField(
        upload_to='images/resized_image',
        max_length=255,
        editable=False,
        verbose_name=_(u"resized"))
    mode = models.CharField(
        choices=MODE_CHOICES,
        editable=False,
        max_length=16,
        verbose_name=_(u"mode"))
    width = models.IntegerField(
        editable=False,
        verbose_name=_(u"width"))
    height = models.IntegerField(
        editable=False,
        verbose_name=_(u"height"))
    error = models.CharField(
        blank=True,
        null=True,
        editable=False,
        max_length=255,
        verbose_name=_(u"error message"))
    crop_x1 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"crop x1"))
    crop_y1 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"crop x1"))
    crop_x2 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"crop x2"))
    crop_y2 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"crop y2"))

    def cropped(self):
        return (self.crop_x1 is not None and
                self.crop_y1 is not None and
                self.crop_x2 is not None and
                self.crop_y2 is not None)
    cropped.boolean = True
    cropped.short_description = _(u"cropped")

    def default_crop(self):
        original_width = self.original_name.width
        original_height = self.original_name.height

        ratio_w = float(self.width) / original_width
        ratio_h = float(self.height) / original_height
        ratio_max = max(ratio_w, ratio_h)

        crop_width = self.width / ratio_max
        crop_height = self.height / ratio_max

        width_offset = (original_width - crop_width) / 2.
        height_offset = (original_height - crop_height) / 2.

        return {"x1": int(width_offset), "y1": int(height_offset), "x2": int(crop_width + width_offset), "y2": int(crop_height + height_offset)}

    def delete(self, *args, **kwargs):
        file = self.resized_name.file
        if file:
            self.resized_name.storage.delete(file)
        return super(ResizedImage, self).delete(*args, **kwargs)
