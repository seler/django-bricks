# -*- coding: utf-8 -*-
from django.db.models.fields.files import ImageField, ImageFieldFile, ImageFileDescriptor
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget

from .forms import CropImageField as CropImageFormField
from .widgets import AdminCropImageFileWidget


class CropImageFieldFile(ImageFieldFile):
    def delete(self, save=True):
        if hasattr(self, '_size_cache'):
            del self._size_cache
        super(CropImageFieldFile, self).delete(save)


class CropImageFileDescriptor(ImageFileDescriptor):
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(CropImageFileDescriptor, self).__set__(instance, value)
        if previous_file is not None and previous_file.name:
            self.field.update_size_field(instance, force=True)
            if isinstance(previous_file, CropImageFieldFile) and isinstance(value, InMemoryUploadedFile):
                delete_original(previous_file)
            delete_resized(previous_file.name)


class CropImageField(ImageField):
    u"""
    Modified Django's `ImageField`. Kasuje fizyczne pliki przy zmianie lub
    usuwaniu obiektu, kasuje powiązane `ResizedImage`.

    Dodaje podgląd zdjęcia oraz link do listy powiązanych `ResizedImage`.
    """
    attr_class = CropImageFieldFile
    descriptor_class = CropImageFileDescriptor
    description = _("Image")

    def __init__(self, verbose_name=None, size_field=None, **kwargs):
        self.size_field = size_field
        super(CropImageField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name):
        super(CropImageField, self).contribute_to_class(cls, name)
        signals.post_init.connect(self.update_size_field, sender=cls)
        signals.pre_delete.connect(self.delete_resized, sender=cls)
        signals.post_delete.connect(self.delete_original, sender=cls)

    def update_size_field(self, instance, force=False, *args, **kwargs):
        if not self.size_field:
            return

        file = getattr(instance, self.attname)
        if not file and not force:
            return

        size_field_filled = self.size_field and getattr(instance, self.size_field)
        if size_field_filled and not force:
            return

        if file:
            size = file.size
        else:
            size = None

        setattr(instance, self.size_field, size)

    def delete_resized(self, instance, *args, **kwargs):
        delete_resized(self.name)

    def delete_original(self, instance, *args, **kwargs):
        file = getattr(instance, self.attname)
        if file and file.name != self.default:
            delete_original(self)

    def formfield(self, **kwargs):
        defaults = {'form_class': CropImageFormField}
        if 'widget' in kwargs and kwargs['widget'] is AdminFileWidget:
            kwargs.update({'widget': AdminCropImageFileWidget})
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)


def delete_resized(original_name):
    from .models import ResizedImage
    map(lambda i: i.delete(), ResizedImage.objects.filter(original_name=original_name))


def delete_original(file):
    file.storage.delete(file)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    rules = [
        (
            (CropImageField,),
            [],
            {
                "size_field": ["size_field", {"default": "'size'"}],
            },
        )
    ]
    add_introspection_rules(rules, ["^bricks\.images\.fields\.CropImageField"])
