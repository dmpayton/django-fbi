# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FacebookAccount'
        db.create_table('django_fbi_facebookaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='facebook', unique=True, null=True, to=orm['auth.User'])),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('facebook_email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True)),
            ('connected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('access_token', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('api_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('django_fbi', ['FacebookAccount'])

        # Adding model 'FacebookApp'
        db.create_table('django_fbi_facebookapp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('connect', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('app_secret', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('permissions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('canvas_template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('canvas_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tab_template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tab_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_fbi', ['FacebookApp'])


    def backwards(self, orm):
        
        # Deleting model 'FacebookAccount'
        db.delete_table('django_fbi_facebookaccount')

        # Deleting model 'FacebookApp'
        db.delete_table('django_fbi_facebookapp')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_fbi.facebookaccount': {
            'Meta': {'ordering': "('user',)", 'object_name': 'FacebookAccount'},
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'api_data': ('django.db.models.fields.TextField', [], {}),
            'connected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'facebook'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'django_fbi.facebookapp': {
            'Meta': {'ordering': "('namespace',)", 'object_name': 'FacebookApp'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'canvas_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'canvas_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'connect': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'permissions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tab_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tab_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_fbi']
