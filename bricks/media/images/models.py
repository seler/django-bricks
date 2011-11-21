from django.db import models
from django.utils.translation import ugettext_lazy as _


class Image(models.Model):
    image = models.ImageField(upload_to='original')

    class Meta:
        db_table = 'bricks_media_image'
        verbose_name = _(u'image')
        verbose_name_plural = _(u'images')

    def __unicode__(self):
        return self.image.name

    @models.permalink
    def get_absolute_url(self):
        return ('bricks.media.images.views.image_detail', (), {'object_id':self.id})
