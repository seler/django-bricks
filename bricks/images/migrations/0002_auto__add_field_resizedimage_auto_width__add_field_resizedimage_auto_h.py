# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ResizedImage.auto_width'
        db.add_column(u'images_resizedimage', 'auto_width',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ResizedImage.auto_height'
        db.add_column(u'images_resizedimage', 'auto_height',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ResizedImage.auto_width'
        db.delete_column(u'images_resizedimage', 'auto_width')

        # Deleting field 'ResizedImage.auto_height'
        db.delete_column(u'images_resizedimage', 'auto_height')


    models = {
        u'bricks.brick': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Brick'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'images.image': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Image', '_ormbases': [u'bricks.Brick']},
            u'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('bricks.images.fields.CropImageField', [], {'size_field': "'size'", 'max_length': '256'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'images.resizedimage': {
            'Meta': {'object_name': 'ResizedImage'},
            'auto_height': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_width': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crop_x1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_x2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_y1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop_y2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'original_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'resized_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['images']