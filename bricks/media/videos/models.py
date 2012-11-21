# -*- coding: utf-8 -*-

import datetime

# importy z django
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bricks.core.models import TiedObject
#from .managers import VideosManager
from .tasks import process_video


safe_storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)
safe_storage = safe_storage_class()

ASPECT_RATIO_CHOICES = (
    (1.33, _(u'4:3')),
    (1.62, _(u'golden ratio')),
    (1.67, _(u'5:3')),
    (1.78, _(u'16:9')),
    (1.85, _(u'US widescreen cinema standard')),
    (2.39, _(u'widescreen cinema standard')),
)


def firstof(*items):
    for i in items:
        if i:
            return i


class Video(TiedObject):
    file = models.FileField(
        blank=True, null=True, storage=safe_storage,
        upload_to='bricks/videos/original',
        verbose_name=_(u'plik'),)

    #TODO: ForeignKey na models bricks.media.images
    screenshot = models.ImageField(
        upload_to='bricks/videos/screenshot',
        blank=True,
        null=True,
        verbose_name=_(u"screenshot"))

    screenshot_time = models.FloatField(
        default=3.,
        help_text=_(u'sekunda, z której zostanie zrobiony kadr'),
        verbose_name=_(u'czas kadru'))

    slug = models.SlugField(verbose_name=_('slug'))

    name = models.CharField(
        max_length=64,
        verbose_name=_(u'nazwa'))

    user = models.ForeignKey('auth.User',
                             verbose_name=_(u'użytkownik dostawca'),
                             related_name='videos')

    width = models.IntegerField(
        blank=True,
        editable=False,
        null=True,
        verbose_name=_(u'szerokość'))

    height = models.IntegerField(
        blank=True,
        editable=False,
        null=True,
        verbose_name=_(u'wysokość'))

    aspect_ratio = models.FloatField(
        blank=True,
        choices=getattr(
            settings, 'ASPECT_RATIO_CHOICES', ASPECT_RATIO_CHOICES),
        null=True,
        verbose_name=_(u'proporcje'))

    duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_(u"czas trwania"))

    ready = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_(u'skonwertowany'))

    #TODO
    #objects = VideosManager()

    class Meta(TiedObject.Meta):
        db_table = 'bricks_media_video'
        verbose_name = _(u'film')
        verbose_name_plural = _(u'filmy')

    def __unicode__(self):
        return self.name

    def _calculate_ratio(self):
        """
        Calculates aspect ratio and returns closest value from
        ``ASPECT_RATIO_CHOICES``.
        """
        ratios = map(lambda l: l[0], getattr(
            settings, 'ASPECT_RATIO_CHOICES', ASPECT_RATIO_CHOICES))
        original_ratio = float(self.width) / float(self.height)
        aspect_ratio = min(ratios, key=lambda x: abs(x - original_ratio))
        return aspect_ratio

    def capture_screenshot(self):
        u"""
        Wywołuje asynchronicznie task zrzucający kadr z filmu
        """
        #TODO
        assert self.id is not None, 'Video object has not been saved!'
        #return capture_frame_task.delay(self.id)

    def process_video(self):
        u"""
        Runs asynchronous function that retrieves info abut video file,
        captures frame and coverts video file.

        Returns asynchrous result.
        """
        assert self.id is not None, 'Video object has not been saved!'
        assert self.file is not None, 'Video has not file attached!'
        return process_video(self.id)

    def get_converted_video(self, format=None):
        u"""
        Returns ConvertedVideo in default format.
        """
        if format is None:
            format = settings.DEFAULT_VIDEO_FORMAT
            try:
                return self.converted_videos.filter(format=format).get()
            except ConvertedVideo.DoesNotExist:
                vs = self.converted_videos.all()[:1]
                if len(vs) > 0:
                    return vs[0]
            return None

    def get_player_width(self):
        return settings.DEFAULT_FORMAT['width']

    def get_player_height(self):
        if self.aspect_ratio:
            return int(round(self.get_player_width() / self.aspect_ratio))
        return settings.DEFAULT_FORMAT['height']

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=True)
            self.converted_videos.all().delete()
            super(Video, self).delete(*args, **kwargs)

    def length(self):
        return str(datetime.timedelta(self.duration))


def converted_video_file_name(instance, filename):
    return '/'.join(['bricks', 'videos', 'converted', str(instance.video.id), filename])


class ConvertedVideo(models.Model):
    FORMAT_CHOICES = tuple(map(lambda item: (item[0], item[1]['name']),
                               settings.BRICKS_VIDEO_FORMATS.items()))

    video = models.ForeignKey('Video',
                              related_name='converted_videos',
                              verbose_name=_(u'film'))

    format = models.PositiveSmallIntegerField(
        choices=FORMAT_CHOICES,
        editable=False,
        verbose_name=_(u'format'))

    file = models.FileField(
        blank=True,
        #editable=False,
        null=True,
        storage=safe_storage,
        upload_to=converted_video_file_name,
        verbose_name=_(u'plik'))

    class Meta:
        db_table = 'bricks_media_convertedvideo'
        unique_together = ('format', 'video')
        verbose_name = _(u'skonwertowany film')
        verbose_name_plural = _('skonwertowane filmy')

    def __unicode__(self):
        return "{0} [{1}]".format(self.video.title, self.get_format_display())

    def get_format(self):
        u"""
        Zwraca słownik formatu
        """
        try:
            return self._format
        except AttributeError:
            self._format = settings.BRICKS_VIDEO_FORMATS.get(self.format)
            return self._format

    def get_width(self):
        try:
            return self.get_format()[self.video.aspect_ratio]['width']
        except:
            return 0

    def get_height(self):
        try:
            return self.get_format()[self.video.aspect_ratio]['height']
        except:
            return 0

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=True)
            super(ConvertedVideo, self).delete(*args, **kwargs)
