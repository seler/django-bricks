# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ArticleSection.object_id'
        db.alter_column(u'articles_articlesection', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'ArticleSection.object_id'
        db.alter_column(u'articles_articlesection', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

    models = {
        u'articles.article': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Article', '_ormbases': [u'bricks.Brick']},
            u'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'articles.articlesection': {
            'Meta': {'object_name': 'ArticleSection'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_sections'", 'to': u"orm['articles.Article']"}),
            'article_section_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
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
        }
    }

    complete_apps = ['articles']