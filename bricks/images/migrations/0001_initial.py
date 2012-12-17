# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table('images_image', (
            ('brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bricks.Brick'], unique=True, primary_key=True)),
            ('image', self.gf('bricks.images.fields.CropImageField')(size_field='size', max_length=256)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('images', ['Image'])

        # Adding model 'ResizedImage'
        db.create_table('images_resizedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_name', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('resized_name', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('auto_width', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('auto_height', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('crop_x1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crop_y1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crop_x2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crop_y2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('images', ['ResizedImage'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table('images_image')

        # Deleting model 'ResizedImage'
        db.delete_table('images_resizedimage')


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
        'images.resizedimage': {
            'Meta': {'object_name': 'ResizedImage'},
            'auto_height': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_width': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crop_x1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_x2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_y1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_y2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'original_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'resized_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['images']