# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table(u'collections_collection', (
            (u'brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bricks.Brick'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'collections', ['Collection'])

        # Adding model 'CollectionObject'
        db.create_table(u'collections_collectionobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collection_objects', to=orm['collections.Collection'])),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('to_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'collections', ['CollectionObject'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table(u'collections_collection')

        # Deleting model 'CollectionObject'
        db.delete_table(u'collections_collectionobject')


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
            u'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'collections.collectionobject': {
            'Meta': {'object_name': 'CollectionObject'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': u"orm['collections.Collection']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
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