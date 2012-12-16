#!/usr/bin/env python
# encoding: utf-8

import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from bricks.models import Brick
from bricks.collections.models import Collection

from .fields import CropImageField

from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.encoding import smart_unicode

from django.contrib.auth.management import create_permissions, _get_all_permissions

# Hack the postsyncdb signal, so we can fix the misbehavior of the
# content_type
# assignment to the proxy models.
# see http://code.djangoproject.com/ticket/11154


def create_permissions_respecting_proxy(app, created_models, verbosity, **kwargs):

    if not kwargs['sender'].__name__ == 'bricks.images.models':
        # if not in 'customer' app, then use the original function
        create_permissions(app, created_models, verbosity, **kwargs)
        return

    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth import models as auth_app
    app_models = get_models(app)
    searched_perms = list()
    ctypes = set()
    for klass in app_models:
        # this is where the difference is: the original create_permissions
        # use ctype = ContentType.objects.get_for_model(klass)
        opts = klass._meta
        ctype, created = ContentType.objects.get_or_create(
            app_label=opts.app_label,
            model=opts.object_name.lower(),
            defaults={'name': smart_unicode(opts.verbose_name_raw)}
        )
        # end of the modification
        ctypes.add(ctype)
        for perm in _get_all_permissions(klass._meta, ctype):
            searched_perms.append((ctype, perm))

    all_perms = set(auth_app.Permission.objects.filter(
        content_type__in=ctypes
    ).values_list("content_type", "codename"))

    for ctype, (codename, name) in searched_perms:
        if(ctype.pk, codename) in all_perms:
            continue
        p = auth_app.Permission.objects.create(
            codename=codename, name=name, content_type=ctype
        )
        if verbosity >= 2:
            print "Adding permission '%s'" % p


post_syncdb.disconnect(
    create_permissions,
    dispatch_uid='django.contrib.auth.management.create_permissions',
)

post_syncdb.connect(
    create_permissions_respecting_proxy,
    dispatch_uid='django.contrib.auth.management.create_permissions',
)


class Gallery(Collection):
    class Meta(Collection.Meta):
        verbose_name = _(u"gallery")
        verbose_name_plural = _(u"galleries")
        proxy = True


class Image(Brick):
    image = CropImageField(
        upload_to='images/original',
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

    def picture(self):
        return self

    def get_absolute_url(self):
        try:
            return self.url
        except AttributeError:
            url = super(Image, self).get_absolute_url()
            if not url:
                from .image import get_image
                #FIXME: tą logikę można by przenieść do get_image
                width = 1920
                height = 1080
                if self.width > width or self.height > height:
                    url = get_image(self.image, ResizedImage.MODE_SCALE, 1920, 1080)
                else:
                    url = self.image.url
            self.url = url
            return url


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
    auto_width = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_(u"auto width"))
    height = models.IntegerField(
        editable=False,
        verbose_name=_(u"height"))
    auto_height = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_(u"auto height"))
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
