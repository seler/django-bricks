import os
import re

from django import template
from django.conf import settings
from django.core.files.storage import get_storage_class

import Image, ImageDraw, ImageFont
from StringIO import StringIO
from django.core.files.base import ContentFile
from pdb import Pdb

register = template.Library()

def generate_image_path(mode, width, height, path):
    return os.path.join('images', str(mode), str(width), str(height), os.path.basename(path))

def generate_error_image(width, height, text=None):
    return 'no-image'

def resize_image(image, mode, width, height):
    original_width, original_height = image.size

    ratio = 1.0
    ratio_w = float(width) / original_width
    ratio_h = float(height) / original_height
    ratio_max = max(ratio_w, ratio_h)

    if mode == 1:
        # crop

        crop_width = width / ratio_max
        crop_height = height / ratio_max

        width_offset = (original_width - crop_width) / 2.
        height_offset = (original_height - crop_height) / 2.

        image = image.crop(map(int, (width_offset, height_offset, crop_width + width_offset, crop_height + height_offset)))

    if mode == 2:
        # reduce

        if ratio_max < 1.0:
            ratio = ratio_max
        else:
            ratio = min(ratio, ratio_w, ratio_h)

        ratio = min(ratio, ratio_w, ratio_h)

        width = original_width * ratio
        height = original_height * ratio

    # crop, reduce, stretch
    return image.resize(map(int, (width, height)), Image.ANTIALIAS).copy()

def generate_new_image(original_image_path, image_path, mode, width, height):
    storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()

    image_file = storage.open(original_image_path)
    image = Image.open(image_file)

    new_image = resize_image(image, mode, width, height)

    # saving image
    fp = StringIO()
    fp.name = image_path
    new_image.save(fp, image.format)
    fp.seek(0)
    cf = ContentFile(fp.read())

    image_path = storage.save(image_path, cf)

    return image_path


class ImageNode(template.Node):
    """
        modes:
        - 1 - crop
        - 2 - reduce
        - 3 - stretch
    """
    def __init__(self, original_image_path, width=None, height=None, mode=None, context_name=None):
        self.original_image_path = template.Variable(original_image_path)
        self.width = width
        self.height = height
        self.mode = mode
        self.context_name = context_name

    def render(self, context):
        original_image_path = self.original_image_path.resolve(context)

        image_path = os.path.join(settings.MEDIA_ROOT, generate_image_path(self.mode, self.width, self.height, original_image_path))

        storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()

        if not storage.exists(image_path):
            if not storage.exists(original_image_path):
                image_path = generate_error_image(self.width, self.height, getattr(settings, 'IMAGE_ERROR_TEXT'), None)
            else:
                image_path = generate_new_image(original_image_path, image_path , self.mode, self.width, self.height)

        result = settings.MEDIA_URL + generate_image_path(self.mode, self.width, self.height, image_path)


        if self.context_name:
            context[self.context_name] = result
            return ''
        else:
            return result

@register.tag
def image(parser, token):
    """Does this and that.

    Syntax::

        {% image <image> [<width>x<height> <mode>] [as <context_name>] %}

    Available modes:

        - ``reduce``

            Reduces original image to given size while maintaining aspect ratio. Given ``width`` and ``height`` are treated as maximal values.

        - ``crop``

            Crops original image to given size.

        - ``stretch``

            Stretches original image to given size discarding aspect ratio.

    Example usage:
    
        ``{% image object.image %}``
        
            Returns url to original sized image.
        
        ``{% image object.image as image_url %}``
        
            Puts url to original sized image into contex as ``image_url``.
            
        ``{% image object.image 100x100 reduce %}``
        
            Return url to reduced image.
            
        ``{% image object.image 100x100 crop as cropped_image_url %}``
        
            Puts url to cropped image into context as ``cropped_image_url``.
        
        ``{% image object.image 100x100 stretch %}``"""

    bits = token.split_contents()

    image = bits[1]

    modes = {'reduce':2, 'crop':1, 'stretch':3}

    if len(bits) == 2:
        return ImageNode(image)
    if len(bits) == 4 and bits[3] == 'as':
        return ImageNode(image, context_name=bits[4])
    if re.match('^\d+[^\d]+\d+$', bits[2]) and len(bits) in (4, 6) and bits[3] in modes:
        width, height = map(int, re.split('[^\d]+', bits[2]))
        if bits[-2] == 'as':
            context_name = bits[-2]
        else:
            context_name = None
        return ImageNode(image, width=width, height=height, mode=modes[bits[3]], context_name=context_name)
    raise template.TemplateSyntaxError('image tag expects a syntax of {% image <image> [<width>x<height> <mode>] [as <context_name>] %}')
