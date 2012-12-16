import os

from django.utils import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders
from .models import Image, ResizedImage
from .image import get_image


class ImageTestCase(unittest.TestCase):
    def setUp(self):
        image = Image()
        image.title = "Test"
        image.slug = "Test"
        image_filename = finders.find("bricks/tests/lena.png")
        image_file = open(image_filename, 'rb')
        image_file_content = ContentFile(image_file.read())
        image.image.save(os.path.basename(image_filename), image_file_content)
        image_file.close()
        image.save()
        self.image = image

    def test_get_image(self):
        resized_image_path = get_image(self.image.image, ResizedImage.MODE_ZOOM, 1920, 1080)
        self.assertTrue(isinstance(resized_image_path, str))
        #self.assertEqual(self.cat.speak(), 'The cat says "meow"')
