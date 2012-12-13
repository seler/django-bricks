# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('bricks_media_video', (
            (u'brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bricks.Brick'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('screenshot_time', self.gf('django.db.models.fields.FloatField')(default=3.0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('aspect_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'videos', ['Video'])

        # Adding model 'ConvertedVideo'
        db.create_table('bricks_media_convertedvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='converted_videos', to=orm['videos.Video'])),
            ('format', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'videos', ['ConvertedVideo'])

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
        u'bricks.brick': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Brick'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'videos.convertedvideo': {
            'Meta': {'unique_together': "(('format', 'video'),)", 'object_name': 'ConvertedVideo', 'db_table': "'bricks_media_convertedvideo'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converted_videos'", 'to': u"orm['videos.Video']"})
        },
        u'videos.video': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Video', 'db_table': "'bricks_media_video'", '_ormbases': [u'bricks.Brick']},
            'aspect_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
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