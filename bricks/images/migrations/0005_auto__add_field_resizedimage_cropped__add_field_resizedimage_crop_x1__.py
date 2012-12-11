# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ResizedImage.cropped'
        db.add_column(u'images_resizedimage', 'cropped',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ResizedImage.crop_x1'
        db.add_column(u'images_resizedimage', 'crop_x1',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'ResizedImage.crop_y1'
        db.add_column(u'images_resizedimage', 'crop_y1',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'ResizedImage.crop_x2'
        db.add_column(u'images_resizedimage', 'crop_x2',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'ResizedImage.crop_y2'
        db.add_column(u'images_resizedimage', 'crop_y2',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


        # Changing field 'ResizedImage.resized_name'
        db.alter_column(u'images_resizedimage', 'resized_name', self.gf('django.db.models.fields.files.ImageField')(max_length=255))

        # Changing field 'ResizedImage.original_name'
        db.alter_column(u'images_resizedimage', 'original_name', self.gf('django.db.models.fields.files.ImageField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'ResizedImage.cropped'
        db.delete_column(u'images_resizedimage', 'cropped')

        # Deleting field 'ResizedImage.crop_x1'
        db.delete_column(u'images_resizedimage', 'crop_x1')

        # Deleting field 'ResizedImage.crop_y1'
        db.delete_column(u'images_resizedimage', 'crop_y1')

        # Deleting field 'ResizedImage.crop_x2'
        db.delete_column(u'images_resizedimage', 'crop_x2')

        # Deleting field 'ResizedImage.crop_y2'
        db.delete_column(u'images_resizedimage', 'crop_y2')


        # Changing field 'ResizedImage.resized_name'
        db.alter_column(u'images_resizedimage', 'resized_name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ResizedImage.original_name'
        db.alter_column(u'images_resizedimage', 'original_name', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.tie': {
            'Meta': {'ordering': "('-pub_date',)", 'unique_together': "(('content_type', 'object_id'), ('slug', 'level'))", 'object_name': 'Tie'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['core.Tie']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'images.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'images.resizedimage': {
            'Meta': {'object_name': 'ResizedImage'},
            'crop_x1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crop_x2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crop_y1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crop_y2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'cropped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'original_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'resized_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['images']