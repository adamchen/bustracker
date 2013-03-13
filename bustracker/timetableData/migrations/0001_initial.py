# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Operator'
        db.create_table('timetableData_operator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('timetableData', ['Operator'])

        # Adding model 'BusRoute'
        db.create_table('timetableData_busroute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bus_services', to=orm['timetableData.Operator'])),
        ))
        db.send_create_signal('timetableData', ['BusRoute'])

        # Adding model 'BusStop'
        db.create_table('timetableData_busstop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('timetableData', ['BusStop'])

        # Adding model 'RouteJourney'
        db.create_table('timetableData_routejourney', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_stop', self.gf('django.db.models.fields.related.OneToOneField')(related_name='journey', unique=True, to=orm['timetableData.RouteStop'])),
            ('weekdays', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturdays', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('timetableData', ['RouteJourney'])

        # Adding model 'RouteStop'
        db.create_table('timetableData_routestop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='route_stops', to=orm['timetableData.BusStop'])),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('next_stop', self.gf('django.db.models.fields.related.OneToOneField')(related_name='previous_stop', unique=True, to=orm['timetableData.RouteStop'])),
        ))
        db.send_create_signal('timetableData', ['RouteStop'])


    def backwards(self, orm):
        # Deleting model 'Operator'
        db.delete_table('timetableData_operator')

        # Deleting model 'BusRoute'
        db.delete_table('timetableData_busroute')

        # Deleting model 'BusStop'
        db.delete_table('timetableData_busstop')

        # Deleting model 'RouteJourney'
        db.delete_table('timetableData_routejourney')

        # Deleting model 'RouteStop'
        db.delete_table('timetableData_routestop')


    models = {
        'timetableData.busroute': {
            'Meta': {'object_name': 'BusRoute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bus_services'", 'to': "orm['timetableData.Operator']"})
        },
        'timetableData.busstop': {
            'Meta': {'object_name': 'BusStop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'timetableData.operator': {
            'Meta': {'object_name': 'Operator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'timetableData.routejourney': {
            'Meta': {'object_name': 'RouteJourney'},
            'first_stop': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'journey'", 'unique': 'True', 'to': "orm['timetableData.RouteStop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saturdays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weekdays': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'timetableData.routestop': {
            'Meta': {'object_name': 'RouteStop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_stop': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'previous_stop'", 'unique': 'True', 'to': "orm['timetableData.RouteStop']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'route_stops'", 'to': "orm['timetableData.BusStop']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['timetableData']