# -*- coding: utf-8 -*-
import os

from django import template

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from StringIO import StringIO
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned
#from django.db.models.fields.files import FileField


register = template.Library()

from django.contrib.staticfiles import finders
from bricks.images.models import Image as BricksImage
from bricks.images.models import ResizedImage


def generate_image_path(mode, width, height, path):
    return os.path.join('images',
                        mode,
                        '{0}x{1}'.format(width, height),
                        os.path.basename(path))

IMAGE_ERROR_TEXT = u"NO IMAGE"


def generate_error_image(image, mode, width=None, height=None):

    image_path = generate_image_path('error', width, height, image.name)

    if width is None:
        width = height
    if height is None:
        height = width

    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    color = (0, 0, 0)

    draw.line((0, 0) + im.size, fill=color)
    draw.line((0, height - 1, width - 1, 0), fill=color)
    draw.rectangle((0, 0, width - 1, height - 1), outline=color)

    font_path = finders.find("bricks/fonts/DejaVuSansMono.ttf")
    font = ImageFont.truetype(font_path, 15)
    text = "{0}x{1}".format(width, height)
    text_pos = (width / 2. - font.getsize(text)[0] / 2. - 1, height / 1.25 - font.getsize(text)[1] / 2. - 1)
    draw.text(text_pos, text, fill=color, font=font)
    text = IMAGE_ERROR_TEXT
    text_pos = (width / 2. - font.getsize(text)[0] / 2. - 1, height / 4. - font.getsize(text)[1] / 2. - 1)
    draw.text(text_pos, text, fill=color, font=font)

    del draw

    # saving image
    fp = StringIO()
    fp.name = image_path
    im.save(fp, 'PNG')
    fp.seek(0)
    cf = ContentFile(fp.read())

    image_path_saved = image.storage.save(image_path, cf)

    return image_path_saved, width, height


def resize_image(image, mode, width, height):
    if width is None and height is None:
        raise ValueError("width and height are both None")

    original_width, original_height = image.size

    ratio = 1.0
    ratio_w = float(width) / original_width
    ratio_h = float(height) / original_height
    ratio_max = max(ratio_w, ratio_h)

    if mode == ResizedImage.MODE_ZOOM:
        # crop

        crop_width = width / ratio_max
        crop_height = height / ratio_max

        width_offset = (original_width - crop_width) / 2.
        height_offset = (original_height - crop_height) / 2.

        image = image.crop(map(int, (width_offset, height_offset, crop_width + width_offset, crop_height + height_offset)))

    if mode == ResizedImage.MODE_SCALE:
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


def create_image(image, mode, width=None, height=None):
    if not image.storage.exists(image):
        raise IOError('Image does not exists in storage')

    new_image_name = generate_image_path(mode, width, height, image.name)

    image.open()
    im = Image.open(image)

    original_width, original_height = im.size

    if width is None:
        width = original_width * height / original_height
    if height is None:
        height = original_height * width / original_width

    new_im = resize_image(im, mode, width, height)

    # saving image
    fp = StringIO()
    fp.name = new_image_name
    new_im.save(fp, im.format)
    fp.seek(0)
    cf = ContentFile(fp.read())

    return image.storage.save(new_image_name, cf), width, height


def get_image(image, mode, width=None, height=None):
    if isinstance(image, BricksImage):
        image = image.image
    """
    if not isinstance(image, FileField):
        pass
        #raise Exception("image object must be instance of FieldFile class")
    """
    if not image:
        raise ValueError("no image")

    if width is None and height is None:
        raise ValueError("width and height are both None")

    filters = {}
    if width is not None:
        filters['width'] = width
    if height is not None:
        filters['height'] = height
    if width is None:
        filters['auto_width'] = True
    if height is None:
        filters['auto_height'] = True

    created = False
    resized_image_queryset = ResizedImage.objects.filter(original_name=image.name, mode=mode, **filters).order_by('-id')
    try:
        resized_image = resized_image_queryset.get()
    except MultipleObjectsReturned:
        resized_image = resized_image_queryset[:1].get()
        map(lambda r: r.delete(), resized_image_queryset[1:])
    except ResizedImage.DoesNotExist:
        resized_image = ResizedImage(original_name=image.name, mode=mode, **filters)
        created = True

    if (created or resized_image.error
            or not resized_image.resized_name.name):
            #or not image.storage.exists(resized_image.resized_name)):

        try:
            resized_image.resized_name, resized_image.width, resized_image.height = create_image(image, mode, width, height)
            resized_image.error = None
        except IOError as e:
            resized_image.resized_name, resized_image.width, resized_image.height = generate_error_image(image, mode, width, height)
            resized_image.error = e.message
        resized_image.save()

    return resized_image.resized_name.url


def crop_image(image, width, height, x1, y1, x2, y2):
    new_image_name = generate_image_path('crop', width, height, image.name)

    image.open()
    im = Image.open(image)

    im = im.crop((x1, y1, x2, y2))

    im = im.resize((width, height), Image.ANTIALIAS).copy()

    # saving image
    fp = StringIO()
    fp.name = new_image_name
    im.save(fp, im.format)
    fp.seek(0)
    cf = ContentFile(fp.read())

    return image.storage.save(new_image_name, cf)
