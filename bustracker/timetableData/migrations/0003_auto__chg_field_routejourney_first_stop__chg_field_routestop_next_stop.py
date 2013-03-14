# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RouteJourney.first_stop'
        db.alter_column('timetableData_routejourney', 'first_stop_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['timetableData.RouteStop']))

        # Changing field 'RouteStop.next_stop'
        db.alter_column('timetableData_routestop', 'next_stop_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['timetableData.RouteStop']))

    def backwards(self, orm):

        # Changing field 'RouteJourney.first_stop'
        db.alter_column('timetableData_routejourney', 'first_stop_id', self.gf('django.db.models.fields.related.OneToOneField')(default=None, unique=True, to=orm['timetableData.RouteStop']))

        # Changing field 'RouteStop.next_stop'
        db.alter_column('timetableData_routestop', 'next_stop_id', self.gf('django.db.models.fields.related.OneToOneField')(default=None, unique=True, to=orm['timetableData.RouteStop']))

    models = {
        'timetableData.busroute': {
            'Meta': {'object_name': 'BusRoute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bus_services'", 'to': "orm['timetableData.Operator']"})
        },
        'timetableData.busstop': {
            'Meta': {'object_name': 'BusStop'},
            'bearing': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
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
            'first_stop': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'journey'", 'unique': 'True', 'null': 'True', 'to': "orm['timetableData.RouteStop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saturdays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weekdays': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'timetableData.routestop': {
            'Meta': {'object_name': 'RouteStop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_stop': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'previous_stop'", 'unique': 'True', 'null': 'True', 'to': "orm['timetableData.RouteStop']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'route_stops'", 'to': "orm['timetableData.BusStop']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['timetableData']