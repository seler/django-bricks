# -*- coding: utf-8 -*-
import re

from django import template

from bricks.images.image import get_image
from bricks.images.models import ResizedImage

register = template.Library()


class ImageNode(template.Node):
    def __init__(self, image, width, height, mode, context_name=None):
        self.image = template.Variable(image)
        self.width = width
        self.height = height
        self.mode = mode
        self.context_name = context_name

    def render(self, context):
        image = self.image.resolve(context)

        result = get_image(image, self.mode, self.width, self.height)

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

    modes = zip(*ResizedImage.MODE_CHOICES)[0]

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
        return ImageNode(image, width=width, height=height, mode=bits[3], context_name=context_name)
    raise template.TemplateSyntaxError('image tag expects a syntax of {% image <image> [<width>x<height> <mode>] [as <context_name>] %}')
