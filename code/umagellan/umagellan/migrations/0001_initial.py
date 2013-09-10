# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('umagellan_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=56)),
        ))
        db.send_create_signal('umagellan', ['UserProfile'])

        # Adding model 'Course'
        db.create_table('umagellan_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('build_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('room_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('section_days', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users_courses', to=orm['auth.User'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=56, null=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('umagellan', ['Course'])

        # Adding model 'Spot'
        db.create_table('umagellan_spot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=12)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=12)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users_spots', to=orm['auth.User'])),
        ))
        db.send_create_signal('umagellan', ['Spot'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('umagellan_userprofile')

        # Deleting model 'Course'
        db.delete_table('umagellan_course')

        # Deleting model 'Spot'
        db.delete_table('umagellan_spot')


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
        'umagellan.course': {
            'Meta': {'object_name': 'Course'},
            'build_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'room_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'section_days': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users_courses'", 'to': "orm['auth.User']"})
        },
        'umagellan.spot': {
            'Meta': {'object_name': 'Spot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '12'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '12'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users_spots'", 'to': "orm['auth.User']"})
        },
        'umagellan.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'home': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['umagellan']