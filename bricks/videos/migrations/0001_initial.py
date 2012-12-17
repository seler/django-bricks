# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('bricks_media_video', (
            ('brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bricks.Brick'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('screenshot_time', self.gf('django.db.models.fields.FloatField')(default=3.0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('aspect_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('videos', ['Video'])

        # Adding model 'ConvertedVideo'
        db.create_table('bricks_media_convertedvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='converted_videos', to=orm['videos.Video'])),
            ('format', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('videos', ['ConvertedVideo'])

        # Adding unique constraint on 'ConvertedVideo', fields ['format', 'video']
        db.create_unique('bricks_media_convertedvideo', ['format', 'video_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ConvertedVideo', fields ['format', 'video']
        db.delete_unique('bricks_media_convertedvideo', ['format', 'video_id'])

        # Deleting model 'Video'
        db.delete_table('bricks_media_video')

        # Deleting model 'ConvertedVideo'
        db.delete_table('bricks_media_convertedvideo')


    models = {
        'bricks.brick': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Brick'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Image']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'images.image': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Image', '_ormbases': ['bricks.Brick']},
            'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('bricks.images.fields.CropImageField', [], {'size_field': "'size'", 'max_length': '256'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'videos.convertedvideo': {
            'Meta': {'unique_together': "(('format', 'video'),)", 'object_name': 'ConvertedVideo', 'db_table': "'bricks_media_convertedvideo'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converted_videos'", 'to': "orm['videos.Video']"})
        },
        'videos.video': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Video', 'db_table': "'bricks_media_video'", '_ormbases': ['bricks.Brick']},
            'aspect_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screenshot_time': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['videos']