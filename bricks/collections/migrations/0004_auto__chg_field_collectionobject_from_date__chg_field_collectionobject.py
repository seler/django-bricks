# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CollectionObject.from_date'
        db.alter_column(u'collections_collectionobject', 'from_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'CollectionObject.to_date'
        db.alter_column(u'collections_collectionobject', 'to_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'CollectionObject.from_date'
        db.alter_column(u'collections_collectionobject', 'from_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'CollectionObject.to_date'
        db.alter_column(u'collections_collectionobject', 'to_date', self.gf('django.db.models.fields.DateTimeField')())

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
        u'collections.collection': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Collection', '_ormbases': [u'bricks.Brick']},
            u'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'collections.collectionobject': {
            'Meta': {'object_name': 'CollectionObject'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': u"orm['collections.Collection']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collections']