from django.forms.fields import ImageField

from .widgets import CropImageFileInput

class CropImageField(ImageField):
    widget = CropImageFileInput
