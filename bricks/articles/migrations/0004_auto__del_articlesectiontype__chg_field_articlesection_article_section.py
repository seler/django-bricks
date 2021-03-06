# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ArticleSectionType'
        db.delete_table('articles_articlesectiontype')


        # Renaming column for 'ArticleSection.article_section_type' to match new field type.
        db.rename_column('articles_articlesection', 'article_section_type_id', 'article_section_type')
        # Changing field 'ArticleSection.article_section_type'
        db.alter_column('articles_articlesection', 'article_section_type', self.gf('django.db.models.fields.PositiveIntegerField')())
        # Removing index on 'ArticleSection', fields ['article_section_type']
        db.delete_index('articles_articlesection', ['article_section_type_id'])


    def backwards(self, orm):
        # Adding index on 'ArticleSection', fields ['article_section_type']
        db.create_index('articles_articlesection', ['article_section_type_id'])

        # Adding model 'ArticleSectionType'
        db.create_table('articles_articlesectiontype', (
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['ArticleSectionType'])


        # Renaming column for 'ArticleSection.article_section_type' to match new field type.
        db.rename_column('articles_articlesection', 'article_section_type', 'article_section_type_id')
        # Changing field 'ArticleSection.article_section_type'
        db.alter_column('articles_articlesection', 'article_section_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.ArticleSectionType']))

    models = {
        'articles.article': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Article', '_ormbases': ['bricks.Brick']},
            'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bricks.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'articles.articlesection': {
            'Meta': {'object_name': 'ArticleSection'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_sections'", 'to': "orm['articles.Article']"}),
            'article_section_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
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
        }
    }

    complete_apps = ['articles']